inp_filename, operation, out_filename = input().split()
# DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE

# reads pgm image
def read_imagefile(f):
    code, width, height, max_level = f.readline().split()
    img_matrix = [] # will be 2d list of lists
    values = f.read().split() # pixel color values of the image

    i=0 # cannot be resetted because it represents the index of a pixel from start (1d not 2d)
    for r in range(int(height)):
        row=[] # for every other row iteration, row list resets
        for c in range(int(width)):
            row.append(int(values[i]))
            i+=1
        img_matrix.append(row) # adds a row to the main list

    return img_matrix

# writes given img_matrix(2d list) to the output file
def write_imagefile(f, img_matrix):
    code, max_level = "P2", "255" # these values do not change for this project
    width = len(img_matrix[0]) # column count
    height = len(img_matrix) # row count
    f.write(f"{code} {width} {height} {max_level}\n") # first line should contain these values in correct order to write a pgm file
    for r in range(height):
        for c in range(width):
            f.write(str(img_matrix[r][c])+" ") # adds each color value with space
        f.write("\n") # newline when row finished

# reverses odd numbered columns
def misalign(img_matrix):
    row = len(img_matrix)
    column = len(img_matrix[0])

    odd_columns=[]

    for r in range(row):
        odd_rows=[]
        for c in range(column):
            if (c+1)%2==1: # gets the value of the odd numbered columns in each row
                odd_rows.append(img_matrix[r][c])
            else:
                odd_rows.append(-1) # for even numbered columns, -1 used as placeholder
        odd_columns.append(odd_rows)

    i=-1
    for r in range(row):
        for c in range(column):
            if (c+1)%2==1: # at odd numbered columns
                img_matrix[r][c]=odd_columns[i][c] #we used i to get the odd columns' values in reversed order
        i+=-1 # decreases i by -1 when moving other row
    
    return img_matrix

# sorts columns in ascending order
def sort_columns(img_matrix):
    row = len(img_matrix)
    column = len(img_matrix[0])

    sorted_columns=[] # stores sorted columns in a 2d way but it stores each sorted column like a row.

    for c in range(column):
        col=[] # resets column list for every other column
        for r in range(row):
            col.append(img_matrix[r][c])
        col.sort() # sorts each column in ascending order
        sorted_columns.append(col)

    for c in range(column):
        for r in range(row):
            img_matrix[r][c]=sorted_columns[c][r] # we reversed the c and r numbers for sorted_columns list because we stored it in a reverse way

    return img_matrix

# rows sorted left to right by respecting the borders
def sort_rows_border(img_matrix):
    row = len(img_matrix)
    column = len(img_matrix[0])

    
    for r in range(row):
        sorted_row=[]
        last_index=0
        for c in range(column):

            # px valued other than 0 added to the sorted_row
            if img_matrix[r][c]!=0:
                sorted_row.append(img_matrix[r][c])

            # border and last px conditions
            if img_matrix[r][c]==0 or c==column-1:
                # to handle more than 1 px thick borders
                if sorted_row==[]:
                    last_index=c+1
                    continue
                sorted_row.sort() # sorts the list contains values until the border or to the end of the line

                # need to separate 0 and end of the line conditions. In 0 cond. we do not include 0 to the sorting but in end of the line cond. we include last px too
                if img_matrix[r][c]==0: 
                    img_matrix[r][last_index:c]=sorted_row
                else:
                    img_matrix[r][last_index:]=sorted_row
                last_index=c+1
                sorted_row=[] # should reset the list because we start sorting values again after the borders

    return img_matrix

# high pass filter
def convolution(img_matrix, kernel):
    row = len(img_matrix)
    column = len(img_matrix[0])
    alt_img_matrix=[] # create another matrix (2d) to make calculations. will make border with zeros to that list to make the calculation properly. If we use a single matrix, results will be altered.

    for r in range(row):
        l_row=[]
        for c in range(column):
            if c==0: # adds 0 to start of the each row
                l_row.append(0)
            l_row.append(img_matrix[r][c])
            if c==column-1: # adds 0 to end of the each row
                l_row.append(0)
        alt_img_matrix.append(l_row)

    alt_img_matrix.insert(0,[0 for _ in range(column+2)]) # adds a full row of 0's at the first row of the edited list
    alt_img_matrix.append([0 for _ in range(column+2)]) # adds a full row of 0's at the end of the edited list

    for r in range(row):
        for c in range(column):
            total_value=0 # total value resets after the calculation with given kernel finishes
            for rk in range(3):
                for ck in range(3):
                    total_value+=(alt_img_matrix[r+rk][c+ck]*kernel[rk][ck]) # calculates the multiplication of the each overlapped matrix element with the each overlapped kernel element and adds all them into total_value
            # pixel value cannot be less than 0 and cannot be more than 255
            if total_value>255:
                total_value=255
            elif total_value<0:
                total_value=0

            img_matrix[r][c]=total_value # writes each calculation result to our non-evaluated list
    
    return img_matrix # returns the resulting list

# DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE
f = open(inp_filename, "r")
img_matrix = read_imagefile(f)
f.close()

if operation == "misalign":
    img_matrix = misalign(img_matrix)

elif operation == "sort_columns":
    img_matrix = sort_columns(img_matrix)

elif operation == "sort_rows_border":
    img_matrix = sort_rows_border(img_matrix)

elif operation == "highpass":
    kernel = [
        [-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1]
    ]
    img_matrix = convolution(img_matrix, kernel)

f = open(out_filename, "w")
write_imagefile(f, img_matrix)
f.close()