"""
Script is called sankey_nuts because anyone has to be bordering on the insane to even attempt to draw this diagram.
I have data for with these dimensions.
Category: {Consortium, Local Authority, Standalone}
Provider: {GLA, DIY, FS, CEM}
Group: {57 different "group" names some of which only contain a single school so aren't really groups.
Schools: 163 different school
#candidates - integer value.

Can I create a Sankey diagram which shows the above proportions?

"""

import pandas as pd
from plotly.offline import plot
import plotly.graph_objects as go


# These functions don't do much but may make the code that follows marginally less UNreadable.
def add_link(src,trg, val, col):
    links.loc[len(links)] = [src,trg, val, col]


def add_node(id, lab, col, tier, size):
    nodes.loc[len(nodes)] = [id, lab, col, tier, size]


def id_of(lab):
    return nodes.loc[(nodes.Label == lab)].values[0, 0]


# Load the data
df = pd.read_csv('data/sankey_nuts.csv')

# Create dictionaries to map colours to RGB/ex codes.
# For convenience, some keys will be assigned the same values.
lcs = {'blue'   :'rgba(73, 148, 206, 0.2)', 'Grammar Consortium': 'rgba(73, 148, 206, 0.2)',
       'orange' :'rgba(255,127,0,0.2)',     'Local Authority': 'rgba(255,127,0,0.2)',
       'green'  :'rgba(127, 194, 65, 0.2)', 'Single School': 'rgba(127, 194, 65, 0.2)',
       'dkorange': 'rgba(250, 188, 19, 1)', 'purple': 'rgba(0,0,255,0.5)'}

ncs = {'blue'   :'#4994CE', 'Grammar Consortium' :'#4994CE',
       'orange' :'#F27420', 'Local Authority' :'#F27420',
       'green'  :'#7FC241', 'Single School' :'#7FC241',
       'grey'   :'#D3D3D3', 'DIY' :'#D3D3D3',
       'purple' :'#8A5988', 'GLA' :'#8A5988',
       'turq'   :'#449E9E', 'FS' :'#449E9E',
       'yellow' :'#FABC13', 'CEM' :'#FABC13'
       }

# Create two empty dataframes row by row. One to contain nodes, the other the links between them.
nodes = pd.DataFrame(columns=['ID', 'Label', 'Colour', 'Tier', 'Size'])
links = pd.DataFrame(columns=['Source', 'Target', 'Value', 'Link Colour'])

# Start by hard coding some colours to use.  This will be deprecated by the above dictionaries but keep this for now ...
nc = '#4994CE'
lc = 'rgba(127, 194, 65, 0.2)'   # 0.2 is the transparency.

# TIER 0. This is the root so we just have to define the node name.
i = 0
root = 'English 11-plus'
nodes.loc[len(nodes)] = [i, root, ncs['grey'], 0, df.tested.sum()]

# TIER 1a & b. This is where it gets interesting(/challenging!)
# Add the three categories to nodes.
# Create a temp dataframe which expands all root × category and sums the number of candidates in each.
tdf = df.groupby('category')['tested'].sum().copy()
tdf = tdf.to_frame()
tdf = tdf.reset_index()
# Could optionally sort this dataframe large=>small, however, in this case it is already in that order.

for cat in tdf.category.unique():
    print(cat)
    i += 1
    arow = tdf.loc[(tdf.category == cat)].values
    count = arow[0, 1]
    nodes.loc[len(nodes)] = [i, cat, ncs[cat], 1, count]
    links.loc[len(links)] = [0, i, count, lcs[cat]]


# TIER 2a. This is where it gets REALLY interesting(/challenging!)
# Create a temp dataframe which expands all category × provider and sums the number of candidates in each.
tdf = df.groupby(['category','provider'])['tested'].sum().copy()
tdf = tdf.to_frame()
tdf = tdf.sort_values(by=['tested'], ascending=False)
tdf = tdf.reset_index()

# iterate over the TARGETs to update the NODES first
for prov in tdf.provider.unique():
    print(prov)
    i += 1
    add_node(i, prov, ncs[prov], 2, tdf.loc[tdf.provider == prov].tested.sum())

# TIER 2b: Iterate over *all* rows in tdf to create correct size links between category => provider.
# (I don't care how much coding purists dislike and object to using iterrows!)
for index, row in tdf.iterrows():
    # print('\nrow is\n', row)
    add_link(id_of(row.category), id_of(row.provider), row.tested, lcs[row.category])

# TIER 3. This is where it gets REALLY interesting(/challenging!)
# Firstly, we have to find proper groups that contain more than one school!
uniques = df['GroupTest'].value_counts()
list_of_groups = uniques[uniques > 1].index.tolist()
tdf = df.groupby(['category', 'provider','GroupTest'])['tested'].sum().copy()
tdf = tdf.to_frame()
# tdf = tdf.sort_values(by=['tested'], ascending=False)
tdf = tdf.reset_index()

for grp in list_of_groups:
    # print(grp)
    i += 1
    cat = tdf.loc[tdf.GroupTest == grp].values[0, 0]
    provider = tdf.loc[tdf.GroupTest == grp].values[0, 1]
    seats = tdf.loc[tdf.GroupTest == grp].values[0, 3]
    add_node(i, grp, ncs[cat], 3, seats)
    # TIER 3b ... and create the links in the same loop as each group test has only one parent.
    add_link(id_of(provider), id_of(grp), seats, lcs[cat])


# TIER 4. Iterate over all 163 schools
# Create nodes entries.
# if the group test value appears in list_of_groups create link from school to group else ...
# create link from school to provider!

for index, row in df.iterrows():
    print('\nrow is\n', row)
    i += 1
    # 4a: Add an entry to the nodes dataframe
    add_node(i, row.loc['Label'], ncs['grey'], 4, row.loc['tested'])
    if row.loc['GroupTest'] in list_of_groups:
        print(row.loc['Label'], 'is part of the real group', row.loc['GroupTest'])
        add_link(id_of(row.loc['GroupTest']), id_of(row.loc['Label']), row.loc['tested'], lcs[row.loc['category']])
    else:
        print(row.loc['Label'], 'is NOT part of a real group')
        add_link(id_of(row.loc['provider']), id_of(row.loc['Label'])  , row.loc['tested'], lcs[row.loc['category']])


# ... if it helps to be able to look at the data ...
# links.to_csv('data/links.csv', index=False)
# nodes.to_csv('data/nodes.csv', index=False)


"""

... for the next mental acrobatics we move on to the 
                                                                     
  o__ __o     o            o__ __o     ____o__ __o____  ____o__ __o____  __o__   o          o        o__ __o     
 <|     v\   <|>          /v     v\     /   \   /   \    /   \   /   \     |    <|\        <|>      /v     v\    
 / \     <\  / \         />       <\         \o/              \o/         / \   / \\o      / \     />       <\   
 \o/     o/  \o/       o/           \o        |                |          \o/   \o/ v\     \o/   o/              
  |__  _<|/   |       <|             |>      < >              < >          |     |   <\     |   <|       _\__o__ 
  |          / \       \\           //        |                |          < >   / \    \o  / \   \\          |   
 <o>         \o/         \         /          o                o           |    \o/     v\ \o/     \         /   
  |           |           o       o          <|               <|           o     |       <\ |       o       o    
 / \         / \ _\o__/_  <\__ __/>          / \              / \        __|>_  / \        < \      <\__ __/>    
                                                                                                                 
                                                                                                                 

See:
https://plotly.com/python/sankey-diagram/
https://plotly.com/python-api-reference/generated/plotly.graph_objects.Sankey.html
"""

# Positioning 190 nodes is challenging but essential. These few lines of code created a "first pass" attempt at
# positioning using a separate dataframe xy. Coordinates are in the range 0 <= [x|y] <= 1.
# X positions are left to right (as you'd expect) and need to match the tiers.
# Y positions are from top to bottom. These are the ones which need adjusting to get the plot looking good.
# The process was to manually edit xy.csv in Excel to modify y-positions, read back into this script and then
# re-run the code to see how the plot is looking.
# The following code really needs running from the line that loads xy.csv AND xy.csv is a very manually created
# file AND this requires a lot of frigging about with the width and height of the layout (AND I created a different
# xy.csv file for a portrait layout.)

xy = pd.DataFrame()
xy['x'] = nodes.Tier / 5
xy['x'] = xy.x + 0.1
xy['y'] = 0.1
# xy.to_csv('data/xy.csv', index=False)

# try playing around in Excel to make this work first ...
xy = pd.read_csv('data/sankey_xy.csv')

SankeyH = go.Figure(go.Sankey(
    # arrangement='fixed',
    arrangement='snap',
    node=dict(pad=10,
              # thickness = 30,
              line=dict(color='black', width=0),
              label=nodes['Label'],
              color=nodes['Colour'],
              # if orientation='v', x and y coordinates are not as expected!
              x=xy['x'],    # !!!!
              y=xy['y'],    # !!!!
              customdata=nodes['Label'],
              # hovertemplate='%{customdata}: %{value}<extra></extra> pupils',
              ),

    link=dict(source=links['Source'].dropna(axis=0, how='any'),
              target=links['Target'].dropna(axis=0, how='any'),
              value=links['Value'].dropna(axis=0, how='any'),
              color=links['Link Colour'].dropna(axis=0, how='any'),
              # customdata=links['HoverInfo'].dropna(axis=0, how='any'),
              # hovertemplate='%{customdata}',

              )
        )
)

SankeyH.update_layout(margin=dict(t=10, b=10, l=10, r=10))


SankeyH.update_layout(
    autosize=False,
    width = 4300,
    height = 2500,)


plot(SankeyH, validate=False)
SankeyH.write_html('data/Sankey.html', auto_open=True)


