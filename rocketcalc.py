import pandas as pd
import os
import sys
import time

start_time = time.time()

# Set current working directory to execution directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Basic usage manipulation
def run():
    temp_string = ""
    while True:
        temp_string = input("Enter name of CSV to calculate or Name of Object you wish to print \
        (enter 'format' for the required format) or exit: ")
        if temp_string == "exit":
            break
        elif "csv" in temp_string and "name" not in temp_string:
            file = temp_string.split(" ")[1]
            name = None
            break
        elif "name" in temp_string and "csv" in temp_string:
            name = temp_string.split(" ")[1]
            file = temp_string.split(" ")[3]
            break
        elif "format" in temp_string:
            print("Proper Formatting -\n    To calculate: \"csv {name of file}\n    To print Name: name {name of object} csv {name of csv}")
        else:
            print("Please enter proper format\n")
    calculate(file, temp_string, name)

# Calculate function for acceleration and resultant
def calculate(file, temp_string, name=None):
    untapped_data = pd.read_csv(file)
    foo = 0
    if "csv " in temp_string and "name " not in temp_string:
        try:
            while (foo <= untapped_data.shape[0]):

                # Indexing the DataFrame
                current_name = untapped_data['object_name'][foo]
                current_mass_grams = untapped_data['object_mass'][foo]
                current_thrust = untapped_data['object_thrust'][[foo]]

                # Convert grams to kilograms = G/1000
                current_mass_kilograms = current_mass_grams / 1000


                # Calculate weight through gravity = KG * 9.8 // Converts to Newtons
                current_weight_n = current_mass_kilograms * 9.8

                # Calculate the resultant force
                current_resultant_force = current_thrust - current_weight_n

                # Calculate the acceleration m/s²
                current_acceleration = current_resultant_force / current_mass_kilograms

                #print(int(current_resultant_force))
                untapped_data.iat[foo, 3] = str(round(float(current_resultant_force), 4)) + " N"
                untapped_data.iat[foo, 4] = str(round(float(current_acceleration), 4)) + " m/s²"
                
                # Pointer
                foo += 1

        except Exception as e:
            untapped_data.to_csv("modified_"+file, index=False)
            os.system("clear")
            time_calculation = round(time.time() - start_time, 2)
            if time_calculation < 1:
                ending = "ms"
            else:
                ending = "mins"
            print(f"Calculations finished\n\n---------LOG---------\n{e}\nTime Taken: {time_calculation}{ending}\n")
    elif "name" in temp_string:
        os.system("clear")
        data = untapped_data.loc[untapped_data['object_name'] == name]
        if "Empty DataFrame" in str(data):
            print(f"No data found for {name}")
        else:
            print("----------------------------------------------------------------")
            print(f"----------------------Data for  {name}------------------------")
            print("----------------------------------------------------------------")
            
            print(str(data))
    else:
        os.system("clear")
        print("Unable to access CSV")


#-----------------------------------------------------------------------
# Arguments
def main():
    
    args = sys.argv[1:]
    try:
        if len(args) >=1:
            if "-csv" in args and "-name" not in args:
                child_location = int(args.index("-csv")) + 1
                file = args[child_location]
                calculate(file, f"csv {file}")
            elif "-name" in args and "-csv" in args:
                child_location_file = int(args.index("-csv")) + 1
                child_location_name = int(args.index("-name")) + 1
                if "-name" not in args[child_location_file] and "-csv" not in args[child_location_name]:
                    file = args[child_location_file]
                    name = args[child_location_name]
                    calculate(file=file, temp_string=(f"name {name} csv {file}"), name=name)
                else:
                    print(f"rocketcalc.py[ Missing argument(1) ]")
            elif args[0] == "-run":
                run()
            else:
                os.system("clear")
                print(f"Unable to access CSV with commands: {args}")
    except Exception as e:
        os.system("clear")
        if "list index" in str(e):
            print(f"rocketcalc.py[ Missing argument(1) ]")
        elif "local variable" in str(e):
            print("rocketcalc.py[ Exit(0) ]")
        else:
            print(f"ERROR: {e}")

    
if __name__ == "__main__":
    main()
