import os
import glob
import pandas as pd

# game_files now contains a list of all file names that end with .EVE in the games folder.
game_files = glob.glob(os.path.join(os.getcwd(), 'games', '*.EVE'))

# Note: There are two sorting functions in Python. To sort in place use list.sort(), not sorted(list) which returns a new list.
game_files.sort()

game_frames = []

for game_file in game_files:
    # print(game_files)
    game_frame = pd.read_csv(game_file, names=[
                             'type', 'multi2', 'multi3', 'multi4', 'multi5', 'multi6', 'event'])
    game_frames.append(game_frame)

games = pd.concat(game_frames)
# print(games)

# Clean Values
games.loc[games['multi5'] == '??', 'multi5'] = ''

# Extract Identifiers
# Each row of data should be associated with the proper game id. This can be accomplished with the extract() function.
# The extract() function returns a DataFrame, so assign this resulting DataFrame to the variable identifiers.
identifiers = games['multi2'].str.extract(r'(.LS(\d{4})\d{5})')
# print(identifiers)

# Forward Fill Identifiers
# The identifiers DataFrame now has two columns. For rows that match the regex, the row has the correct extracted values.
# We need these values to be filled in for all rows on the identifiers DataFrame.
identifiers = identifiers.fillna(method='ffill')

# Rename Column
identifiers.columns = ['game_id', 'year']
# print(identifiers)

# Concatenate Identifier Columns
games = pd.concat([games, identifiers], axis=1, sort=False)

# Fill NaN Values
games = games.fillna(' ')

# Categorical Event Type
# To slightly reduce the memory used by the games DataFrame we can provide Pandas with a clue to what data is contained in certain columns.
# The type column of our games DataFrame only contains one of six values - info, start, play, com, sub, and data. Pandas can optimize this column with Categorical().
games.loc[:, 'type'] = pd.Categorical(games.loc[:, 'type'])

print(games.head())
