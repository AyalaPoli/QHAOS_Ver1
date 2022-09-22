import os
import csv
def replace_raw_in_csv_old(input_file, new_row,row_index):
    df = pd.read_csv(input_file)
    df.loc[row_index]=new_row
    df.to_csv(input_file,index=False)

def replace_raw_in_csv(input_file, new_row, row_index):
    new_row_str=",".join([str(i) for i in new_row])+"\n"
    output_file="tmp.csv"
    print("input_file {}".format(input_file))
    curr_count=1
    with open(input_file, 'r') as infile, open(output_file, 'a') as outfile:
        for line in infile:
            if curr_count==row_index:
                outfile.write(new_row_str)
            else:
                outfile.write(line)
            curr_count+=1

    with open(output_file, 'r') as infile, open(input_file, 'w') as outfile:
        for line in infile:
            outfile.write(line)
    os.remove(output_file)

input_file= "txt_sending_file.txt"
new_row=["a","b","c"]

if __name__ == '__main__':
    replace_raw_in_csv(input_file, new_row, 2)