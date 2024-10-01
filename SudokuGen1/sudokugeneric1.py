import pandas as pd

# Define the file URL
file_url = "https://raw.githubusercontent.com/gabrield03/SudokuSeries/refs/heads/main/Games/easySudokuPuzzles.txt"

# Read the file using pandas
df = pd.read_csv(file_url, header=None)
print(df.head())  # Print first few lines of the file


# Select a game
# There is 1 puzzle on each line of the file. 1011 lines (games)
count = 0
game = [0]

with open(easy_puzzles, 'r') as file:
  for line in file:
    count += 1
    if count == 1:
      game = line

game = list(game[:-1])

for i in range(len(game)):
  if game[i] == '.':
    game[i] = 0
  else:
    game[i] = int(game[i])

print(game)



# Draw the Game Board
# Draws the current game board
def draw_borders(typeOfLine):
  if typeOfLine == 'border':
    print(f'-------------------------------------')
  elif typeOfLine == 'empty':
    print(f'|           |           |           |')


def draw_board(currIndices):
  draw_borders('border')

  for i in range(len(currIndices)):
    if (i + 1) % 3 != 0:
      if i == 0 or i % 9 == 0:
        print(f'| {currIndices[i]} ', end = '')
      elif i % 3 == 0:
        print(f' {currIndices[i]} ', end = '')
      else:
        print(f'  {currIndices[i]} ', end = '')

    elif (i + 1) % 9 == 0:
      print(f'  {currIndices[i]} |')
      if (i + 1) % 27 == 0:
        draw_borders('border')
      else:
        draw_borders('empty')

    else:
      print(f'  {currIndices[i]} |', end = '')

draw_board(game)


# Initialize the Game Board Values and Possible Values
def create_board_possibilities(game):
  boardPossibilities = {}

  for i in range(81):
    boardPossibilities[i] = list(range(1, 10))

  for given in range(len(game)):
    if game[given] != 0:
      boardPossibilities[given] = [game[given]]

  return boardPossibilities

def make_rows(index):
  selRow = int(index / 9) * 9
  rows = range(selRow, (selRow + 9))

  return rows

def make_cols(index):
  selCol = (index % 9)
  cols = range(selCol, 81, 9)

  return cols

def make_subgrids(index):
  # Find row
  gridRow = int(index / 9)
  if 0 <= gridRow < 3: gridRow = 0
  elif 3 <= gridRow < 6: gridRow = 3
  else: gridRow = 6

  # Find col
  gridCol = index % 9
  if 0 <= gridCol < 3: gridCol = 0
  elif 3 <= gridCol < 6: gridCol = 3
  else: gridCol = 6

  gridStart = (9 * gridRow) + gridCol

  subgrids = list(range(gridStart, (gridStart + 3)))
  subgrids.extend(list(range((gridStart + 9), ((gridStart + 12)))))
  subgrids.extend(list(range((gridStart + 18), ((gridStart + 21)))))

  return subgrids


# Check if the Board is Solved
# Check if the board is solved
def check_status(game):
  if 0 in game:
    return False
  return True


# Iterate Through the Board
# Iterate through

def remove_extra_values(game, boardPossibilities):
  boardWasUpdated = True

  while boardWasUpdated:
    boardWasUpdated = False

    for index in range(len(game)):
      if game[index] != 0:

        # IDENTIFY AND REMOVE DUPLICATE VALUES IN ROWS
        rows = make_rows(index)

        for row in rows:
          if game[index] in boardPossibilities[row] and len(boardPossibilities[row]) > 1:
            boardPossibilities[row].remove(game[index])
            boardWasUpdated = True

        # IDENTIFY AND REMOVE DUPLICATE VALUES IN COLUMNS
        cols = make_cols(index)

        for col in cols:
          if game[index] in boardPossibilities[col] and len(boardPossibilities[col]) > 1:
            boardPossibilities[col].remove(game[index])
            boardWasUpdated = True

        # IDENTIFY AND REMOVE DUPLICATE VALUES IN SUBGRIDS
        subgrids = make_subgrids(index)

        for subgrid in subgrids:
          if game[index] in boardPossibilities[subgrid] and len(boardPossibilities[subgrid]) > 1:
            boardPossibilities[subgrid].remove(game[index])
            boardWasUpdated = True

  # Update the board with the new boardPossibilities
  for val in range(len(boardPossibilities)):
    if len(boardPossibilities[val]) == 1 and game[val] == 0:
      game[val] = boardPossibilities[val][0]

  return game, boardPossibilities

# Find isolated values in rows, columns, and grids

def remove_isolated_values(game, boardPossibilities):
  boardWasUpdated = True

  while boardWasUpdated:
    boardWasUpdated = False

    for index in range(len(game)):
      if game[index] != 0:

        # IDENTIFY AND REMOVE DUPLICATE VALUES IN ROWS, COLUMNS, AND SUBGRIDS
        rows = make_rows(index)
        cols = make_cols(index)
        subgrids = make_subgrids(index)

        for num in range(1, 10):
          rowCount = 0
          rowIsoNumIndex = -1

          colCount = 0
          colIsoNumIndex = -1

          subgridCount = 0
          subgridIsoNumIndex = -1

          for row in rows:
            if num in boardPossibilities[row] and len(boardPossibilities[row]) == 1:
              rowCount = 10

            elif num in boardPossibilities[row] and rowCount == 0:
              rowIsoNumIndex = row
              rowCount += 1
            elif num in boardPossibilities[row] and rowCount != 0:
              rowCount += 1


          for col in cols:
            if num in boardPossibilities[col] and len(boardPossibilities[col]) == 1:
              colCount = 10

            elif num in boardPossibilities[col] and colCount == 0:
              colIsoNumIndex = col
              colCount += 1
            elif num in boardPossibilities[col] and colCount != 0:
              colCount += 1


          for subgrid in subgrids:
            if num in boardPossibilities[subgrid] and len(boardPossibilities[subgrid]) == 1:
              subgridCount = 10

            elif num in boardPossibilities[subgrid] and subgridCount == 0:
              subgridIsoNumIndex = subgrid
              subgridCount += 1
            elif num in boardPossibilities[subgrid] and subgridCount != 0:
              subgridCount += 1


          # Replace isolated values in rows
          if rowCount == 1 and rowIsoNumIndex != -1:
            boardPossibilities[rowIsoNumIndex] = [num]
            boardWasUpdated = True

          # Replace isolated values in cols
          if colCount == 1 and colIsoNumIndex != -1:
            boardPossibilities[colIsoNumIndex] = [num]
            boardWasUpdated = True

          # Replace isolated values in subgrids
          if subgridCount == 1 and subgridIsoNumIndex != -1:
            boardPossibilities[subgridIsoNumIndex] = [num]
            boardWasUpdated = True

    if boardWasUpdated:
      game, boardPossibilities = remove_extra_values(game, boardPossibilities)

  return game, boardPossibilities


# Advanced Implementation
# Identify tuples (doubles, triples, etc.)
def identify_tuples(game, boardPossibilities):
  boardWasUpdated = True

  while boardWasUpdated:
    boardWasUpdated = False

    for index in range(len(game)):
      if game[index] != 0:

        # IDENTIFY AND REMOVE DUPLICATE VALUES IN ROWS, COLUMNS, AND SUBGRIDS
        rows = make_rows(index)
        cols = make_cols(index)
        subgrids = make_subgrids(index)

        tuples = {2: [], 3: []}
        # Future implementation
        # tuples = {2: [], 3: [], 4: [], 5: []}

        pairsToRemove = []
        triplesToRemove = []

        # ROW TUPLES
        # Add tuples with size > 1
        for row in rows:
          if len(boardPossibilities[row]) == 2: tuples[2].append(boardPossibilities[row])
          elif len(boardPossibilities[row]) == 3: tuples[3].append(boardPossibilities[row])

        for size, val in tuples.items():
          # Pairs
          if len(val) > size and size == 2: # If len(val) < size, we ignore it -- not enough groupings

            tempTuple = val.copy()
            for tup in val:
              tempTuple.remove(tup)
              if tup in tempTuple:
                pairsToRemove.append(tup)

          # Triples
          elif len(val) > size and size == 3:

            tempTuple = val.copy()
            for tup in val:
              tempTuple.remove(tup)
              tempTuple2 = tempTuple.copy()
              if tup in tempTuple2:
                tempTuple2.remove(tup)
                if tup in tempTuple2:
                  triplesToRemove.append(tup)

        # Iterate over the row once more, removing nums if they are in the pair
        for nums in pairsToRemove:
          for row in rows:
            if len(boardPossibilities) > 2 and nums[0] in boardPossibilities[row]:
              boardPossibilities[row].remove(nums[0])
              boardWasUpdated = True
            if nums[0] not in boardPossibilities[row] and len(boardPossibilities) > 1 and nums[1] in boardPossibilities[row]:
              boardPossibilities[row].remove(nums[1])
              boarWasUpdated = True

        for nums in triplesToRemove:
          for row in rows:
            if len(boardPossibilities) > 3 and nums[0] in boardPossibilities[row]:
              boardPossibilities[row].remove(nums[0])
              boardWasUpdated = True
            if nums[0] not in boardPossibilities[row] and len(boardPossibilities) > 2 and nums[1] in boardPossibilities[row]:
              boardPossibilities[row].remove(nums[1])
              boarWasUpdated = True
            if nums[0] not in boardPossibilities[row] and nums[1] not in boardPossibilities[row] and len(boardPossibilities) > 1 and nums[2] in boardPossibilities[row]:
              boardPossibilities[row].remove(nums[2])
              boarWasUpdated = True


        # Reset variables for col processing
        tuples = {2: [], 3: []}
        # Future implementation
        # tuples = {2: [], 3: [], 4: [], 5: []}

        pairsToRemove = []
        triplesToRemove = []

        # COLUMN TUPLES
        # Add tuples with size > 1
        for col in cols:
          if len(boardPossibilities[col]) == 2: tuples[2].append(boardPossibilities[col])
          elif len(boardPossibilities[col]) == 3: tuples[3].append(boardPossibilities[col])

        for size, val in tuples.items():
          # Pairs
          if len(val) > size and size == 2: # If len(val) < size, we ignore it -- not enough groupings

            tempTuple = val.copy()
            for tup in val:
              tempTuple.remove(tup)
              if tup in tempTuple:
                pairsToRemove.append(tup)

          # Triples
          elif len(val) > size and size == 3:

            tempTuple = val.copy()
            for tup in val:
              tempTuple.remove(tup)
              tempTuple2 = tempTuple.copy()
              if tup in tempTuple2:
                tempTuple2.remove(tup)
                if tup in tempTuple2:
                  triplesToRemove.append(tup)

        # Iterate over the row once more, removing nums if they are in the pair
        for nums in pairsToRemove:
          for col in cols:
            if len(boardPossibilities) > 2 and nums[0] in boardPossibilities[col]:
              boardPossibilities[col].remove(nums[0])
              boardWasUpdated = True
            if nums[0] not in boardPossibilities[col] and len(boardPossibilities) > 1 and nums[1] in boardPossibilities[col]:
              boardPossibilities[col].remove(nums[1])
              boarWasUpdated = True

        for nums in triplesToRemove:
          for col in cols:
            if len(boardPossibilities) > 3 and nums[0] in boardPossibilities[col]:
              boardPossibilities[col].remove(nums[0])
              boardWasUpdated = True
            if nums[0] not in boardPossibilities[col] and len(boardPossibilities) > 2 and nums[1] in boardPossibilities[col]:
              boardPossibilities[col].remove(nums[1])
              boarWasUpdated = True
            if nums[0] not in boardPossibilities[col] and nums[1] not in boardPossibilities[col] and len(boardPossibilities) > 1 and nums[2] in boardPossibilities[col]:
              boardPossibilities[col].remove(nums[2])
              boarWasUpdated = True


        # Reset variables for grid processing
        tuples = {2: [], 3: []}
        # Future implementation
        # tuples = {2: [], 3: [], 4: [], 5: []}

        pairsToRemove = []
        triplesToRemove = []

        # SUBGRID TUPLES
        # Add tuples with size > 1
        for subgrid in subgrids:
          if len(boardPossibilities[subgrid]) == 2: tuples[2].append(boardPossibilities[subgrid])
          elif len(boardPossibilities[subgrid]) == 3: tuples[3].append(boardPossibilities[subgrid])

        for size, val in tuples.items():
          # Pairs
          if len(val) > size and size == 2: # If len(val) < size, we ignore it -- not enough groupings

            tempTuple = val.copy()
            for tup in val:
              tempTuple.remove(tup)
              if tup in tempTuple:
                pairsToRemove.append(tup)

          # Triples
          elif len(val) > size and size == 3:

            tempTuple = val.copy()
            for tup in val:
              tempTuple.remove(tup)
              tempTuple2 = tempTuple.copy()
              if tup in tempTuple2:
                tempTuple2.remove(tup)
                if tup in tempTuple2:
                  triplesToRemove.append(tup)

        # Iterate over the row once more, removing nums if they are in the pair
        for nums in pairsToRemove:
          for subgrid in subgrids:
            if len(boardPossibilities) > 2 and nums[0] in boardPossibilities[subgrid]:
              boardPossibilities[subgrid].remove(nums[0])
              boardWasUpdated = True
            if nums[0] not in boardPossibilities[subgrid] and len(boardPossibilities) > 1 and nums[1] in boardPossibilities[subgrid]:
              boardPossibilities[subgrid].remove(nums[1])
              boarWasUpdated = True

        for nums in triplesToRemove:
          for subgrid in subgrids:
            if len(boardPossibilities) > 3 and nums[0] in boardPossibilities[subgrid]:
              boardPossibilities[subgrid].remove(nums[0])
              boardWasUpdated = True
            if nums[0] not in boardPossibilities[subgrid] and len(boardPossibilities) > 2 and nums[1] in boardPossibilities[subgrid]:
              boardPossibilities[subgrid].remove(nums[1])
              boarWasUpdated = True
            if nums[0] not in boardPossibilities[subgrid] and nums[1] not in boardPossibilities[subgrid] and len(boardPossibilities) > 1 and nums[2] in boardPossibilities[subgrid]:
              boardPossibilities[subgrid].remove(nums[2])
              boarWasUpdated = True







    if boardWasUpdated:
      game, boardPossibilities = remove_extra_values(game, boardPossibilities)

  return game, boardPossibilities



# Identify groupings
def identify_misc_groupings(game, boardPossibilities):


  return game, boardPossibilities



# Solving the Board
def solve_board(game):
  DEBUG = True
  boardComplete = False
  iterations = 0

  # initial board
  print('initial board')
  draw_board(game)

  # Create the board of possibilities:
  boardPossibilities = {}
  boardPossibilities = create_board_possibilities(game)

  # Loop while the board remains incomplete - stop at 10 iterations
  while not boardComplete and iterations < 10:
    # Keep count of the iterations -- too many and we quit because it isn't getting solved
    iterations +=1

    # Remove extra values
    game, boardPossibilities = remove_extra_values(game, boardPossibilities)

    # Remove isolated values
    game, boardPossibilities = remove_isolated_values(game, boardPossibilities)

    # Don't need to match pairs, triplets, etc?
    game, boardPossibilities = identify_tuples(game, boardPossibilities)

    boardComplete = check_status(game)


  if DEBUG:
    # DEBUG - ROWS
    print(f'\n\n---------------------------------------')
    print(f'---------------------------------------')
    print('ROW BOARD POSSIBILITIES')
    count = 0
    for v in boardPossibilities.values():
        if count % 9 == 0:
            print()
        print(v)
        count += 1

    # DEBUG - COLS
    print(f'\n\n---------------------------------------')
    print(f'---------------------------------------')
    print('COLUMN BOARD POSSIBILITIES')
    for colFormat in range(9):
      for k, v in boardPossibilities.items():
        if k % 9 == colFormat:
          print(v)
      print()

    # DEBUG - GRID
    print(f'\n\n---------------------------------------')
    print(f'---------------------------------------')
    print('SUBGRID BOARD POSSIBILITIES')
    for subgridIndex in range(0, 61, 3):
      subgrid = []
      if subgridIndex == 0 or subgridIndex == 3 or subgridIndex == 6 \
        or subgridIndex == 27 or subgridIndex == 30 or subgridIndex == 33 \
        or subgridIndex == 54 or subgridIndex == 57 or subgridIndex == 60:

        subgrid = list(range(subgridIndex, (subgridIndex + 3)))
        subgrid.extend(list(range((subgridIndex + 9), ((subgridIndex + 12)))))
        subgrid.extend(list(range((subgridIndex + 18), ((subgridIndex + 21)))))

        for g in subgrid:
          print(boardPossibilities[g])

        print()

  if not boardComplete:
    print('\nBoard could not be solved. Final board:\n')
    draw_board(game)

  else:
    print('\nThe board was solved! Final board:\n')
    draw_board(game)

solve_board(game)