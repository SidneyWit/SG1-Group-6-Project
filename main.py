# We used Python via Thonny IDE and PyCharm for this project.
# Worked on by CJ Keil, John Lowrie, Sharmin Akter Meera, Kavion Norman, Sidney Wittenberg
# This project was started on 10/4/26
# Major revision on on 10/5/26
# Major revision on on 10/5/26
# Major revision on on 10/7/26
# Major revision on on 10/9/26
# Major revision on on 10/16/26

# CMP SCI 4500 Introduction to the Software Profession

# This program reads and validates a text file containing 0 and 1 and convert it into a black-and-white PNG image
# Then displays this image alongside a provided image2
# Next it searches image2 for a specific pluspattern, and prints how many times the pattern appears and its coordinates
# Lastly creates and displays that an image called image3 in which the white pixels arouund each detected pattern are changed to red

# External files used: 
# IMAGE2.PNG  
# binary txt file that user provides name of
# Image1Converter.py  
# Image2Converter.py

# External files created
# Image3.png
# Image1.png

# John used Thonny and VSCode for this project
# Sources used
# how to open a file https://www.geeksforgeeks.org/python/how-to-read-from-a-file-in-python/
# stack overflow article about comparing arrays https://stackoverflow.com/questions/25532983/finding-identical-rows-and-columns-in-a-numpy-array/66999181
# stack overflow for converting image to arrays in greyscale  https://stackoverflow.com/questions/55826900/grayscale-png-to-numpy-array
# another grey scale article https://stackoverflow.com/questions/52232068/how-to-change-an-image-to-grayscale-represented-as-a-numpy-array
# pillow image interaction https://pillow.readthedocs.io/en/stable/handbook/tutorial.html

#The main data structure is the binary array that represents image 2 where black is 0 and white is 1



from PIL import Image
import numpy as np


# This is the chatgpt generated function it validates that the inputed file name is a proper file name 
# and return the file name as a string 
def GetTextFileName():
    # This function was developed using ChatGPT, as required by the SG1 specification.

    # Windows does not allow these characters in filenames.
    invalid_characters = '<>:"/\\|?*'

    # Windows also reserves these device names, regardless of extension.
    reserved_names = {
        "CON", "PRN", "AUX", "NUL",
        "COM1", "COM2", "COM3", "COM4", "COM5",
        "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5",
        "LPT6", "LPT7", "LPT8", "LPT9"
    }

    while True:
        filename = input("Enter the name of the text file: ")

        # Reject an empty filename.
        if filename == "":
            print("Error: You must enter a filename.")
            continue

        # The filename must end in .txt, without regard to capitalization.
        if not filename.lower().endswith(".txt"):
            print("Error: The filename must end with '.txt'.")
            continue

        # Check for characters that Windows does not permit.
        bad_character = next(
            (char for char in invalid_characters if char in filename),
            None
        )

        if bad_character is not None:
            print(
                f"Error: The filename contains the invalid character "
                f"'{bad_character}'. Windows filenames cannot contain "
                f"the characters < > : \" / \\ | ? *."
            )
            continue

        # Windows filenames cannot end with a space or period.
        # This also catches a name such as "example.txt. ".
        if filename.endswith(" ") or filename.endswith("."):
            print(
                "Error: A Windows filename cannot end with a space or period."
            )
            continue

        # Check the filename portion before ".txt" against reserved names.
        base_name = filename[:-4]

        if base_name.upper() in reserved_names:
            print(
                f"Error: '{base_name}' is a reserved Windows device name "
                "and cannot be used as a filename."
            )
            continue

        # A filename consisting only of ".txt" has no actual name.
        if base_name == "":
            print("Error: You must provide a filename before '.txt'.")
            continue

        return filename
        
# Meera's task: Print a valid binary text file and convert it
# into IMAGE1.PNG, preserving the order of rows and columns.
#
# IDE: PyCharm
# Development date: 10/9/26, 10/13/26, 10/14/26, 10/15/26, 10/16/26
#
# Data structures:
# rows is a list of strings containing the binary text lines.
# pixel_values is a list containing brightness values:
# 0 for black and 255 for white.
# image1 holds the resulting Pillow image.
#
# External files:
# Input: A previously validated binary text file.
# Output: IMAGE1.PNG in the current working directory.
# An existing IMAGE1.PNG is overwritten.


from PIL import Image


class Image1Converter:
    # Stores the name of the validated input file.
    # Parameters: filename is the binary text file's name.
    # Global variables used: None.
    # Returns: None.
    def __init__(self, filename):
        self.filename = filename
        self.image1 = None

    # Prints the text, converts it to pixels, saves and displays IMAGE1.
    # Parameters: None other than self, the current object.
    # Global variables used: None.
    # Returns: The Pillow image stored in self.image1.
    # The input file must already have passed binary file validation.
    # File errors are passed to the calling program.
    def ConvertImage1(self):
        # Reopen the file so reading begins at the first line.
        # Remove only newline characters, preserving the binary data.
        with open(self.filename, "r") as file:
            rows = [line.rstrip("\r\n") for line in file]

        # Print each text row in its original order.
        for row in rows:
            print(row)

        width = len(rows[0])
        height = len(rows)

        # Build the pixel list from left to right, then top to bottom.
        pixel_values = []
        for row in rows:
            for character in row:
                if character == "0":
                    pixel_values.append(0)
                else:
                    pixel_values.append(255)

        # L mode stores one grayscale brightness value per pixel.
        # Only 0 and 255 are used, making the image black and white.
        self.image1 = Image.new("L", (width, height))
        self.image1.putdata(pixel_values)

        # Saving with the same filename overwrites an existing image.
        self.image1.save("IMAGE1.PNG")
        self.image1.show()

        return self.image1

# Meera's task: Load and display IMAGE2.png and convert its
# pixels into an array containing 0 for black and 1 for nonzero.
#
# IDE: PyCharm
# Dates: 10/9/26, 10/13/26, 10/14/26, 10/15/26, 10/16/26
#
# Data structures:
# image2 holds the grayscale image.
# ZerosAndOnes is a two dimensional NumPy array of integers.
# Each entry corresponds to one image pixel at [row, column].
#
# External file: IMAGE2.png in the current working directory.

from PIL import Image
import numpy as np


class Image2Converter:
    # Sets the filename and prepares the image and array attributes.
    # Parameters: filename is the input image filename.
    # Global variables used: None.
    # Returns: None.
    def __init__(self, filename="IMAGE2.png"):
        self.filename = filename
        self.image2 = None
        self.ZerosAndOnes = None

    # Loads and displays IMAGE2 and converts its pixels to binary values.
    # Parameters: None other than self, the current object.
    # Global variables used: None.
    # Returns: The two dimensional ZerosAndOnes array.
    # File errors are passed to the calling program.
    def ConvertImage2(self):
        # Grayscale uses one brightness value for each pixel.
        with Image.open(self.filename) as image:
            self.image2 = image.convert("L")

        self.image2.show()

        # Preserves the original order of the rows and columns.
        pixels = np.array(self.image2)

        # Zero becomes 0. Every nonzero brightness becomes 1.
        self.ZerosAndOnes = (pixels != 0).astype(int)

        return self.ZerosAndOnes


if __name__ == "__main__":
    try:
        converter = Image2Converter()
        ZerosAndOnes = converter.ConvertImage2()

        print("IMAGE2 has been displayed and converted.")
        print("Rows:", ZerosAndOnes.shape[0])
        print("Columns:", ZerosAndOnes.shape[1])

    except FileNotFoundError:
        print("Error: IMAGE2.png was not found in the current directory.")

    except PermissionError:
        print("Error: Permission denied when opening IMAGE2.png.")

    except OSError as error:
        print("Error: Could not read IMAGE2.png:", error)

    input("Press ENTER to end the program.")


    
# This Function checks if the inputted argument of a file has less than 20 chars per line, has at least 10 lines has lines that dont contain 1 or 0, if
# every line has the same ammount of chars. If one of those condition is met then it returns false  otherwise it returns true
def ValidateBinaryFile(file):
    numberOfLines = 0
    includesNon0or1 = False
    lineLessThan20Chars = False
    linesHaveDifferingAmmountOfCharacters = False
    numberOfCharsPerLine = -1

    for line in file:
        
# This is to get rid of newlines 
        lineWithoutEndline = line.rstrip("\r\n")

# -1 is  to make shure this only runs once and each row should be the same size so we only need to set it once
        if(numberOfCharsPerLine == -1):
            numberOfCharsPerLine = len(lineWithoutEndline) 

        
        if(len(lineWithoutEndline) < 20):
            lineLessThan20Chars = True
        
        if(len(lineWithoutEndline) != numberOfCharsPerLine):
            linesHaveDifferingAmmountOfCharacters = True

# any(c not in "01" for c in lineWithoutEndline just checks is any character in the string not 0 or 1
        if any(c not in "01" for c in lineWithoutEndline):
            includesNon0or1 = True
        
        numberOfLines += 1

        
    if(includesNon0or1):
        print("File contains non 1 or 0 characters")
        input("Press Enter to continue...")
        return False
    elif(lineLessThan20Chars):
        print("File contains line with less than 20 characters")
        input("Press Enter to continue...")
        return False
    elif(linesHaveDifferingAmmountOfCharacters):
        print("File contains lines with differing ammounts of characters")
        input("Press Enter to continue...")
        return False
    elif(numberOfLines < 10):
        print("File contains less than 10 lines")
        input("Press Enter to continue...")
        return False

    return True
     
    
# This Function opens IMAGE2.PNG check it for the 11 x 11 plus pattern then prints the midpoint for each pluss and creates IMAGE3.PNG
# where the white background for each plus is turned red. There is no returned value

def CreateImage3():
# The Convert L makes the image greyscale so the values  can be easily converted to 0 and 1 since grey scale images only need 1 value for the alpha channel instead of 3 for RGB
    image2 = Image.open("./" + "IMAGE2.png").convert("L")
        
    pixels = np.array(image2)

# This checks if a pixle is 0 since white would be 256 so if a pixle is above 0 then it gets converted to true and 0 gets converted to false
# Then .astype(int) convets true and false to 0 and 1
    ZerosAndOnes = (pixels != 0).astype(int)
    
    height, width = 250, 250

    pattern = [
        [1,1,1,1,1,0,1,1,1,1,1],
        [1,1,1,1,1,0,1,1,1,1,1],
        [1,1,1,1,1,0,1,1,1,1,1],
        [1,1,1,1,1,0,1,1,1,1,1],
        [1,1,1,1,1,0,1,1,1,1,1],
        [0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,0,1,1,1,1,1],
        [1,1,1,1,1,0,1,1,1,1,1],
        [1,1,1,1,1,0,1,1,1,1,1],
        [1,1,1,1,1,0,1,1,1,1,1],
        [1,1,1,1,1,0,1,1,1,1,1]
    ]
    
    matches = []
        
# This for loop checks each pixle 11 spaces ahead and down for the pattern varible
    for row in range(height - 10):
        for col in range(width - 10):
            section = ZerosAndOnes[row:row + 11, col:col + 11]

            if np.array_equal(section, pattern):
                center_x = col + 5
                center_y = row + 5
                matches.append((center_x, center_y))

    print("Plus pattern found", len(matches), "times at", matches)

    image3 = Image.open("./" + "IMAGE2.png").convert("RGB")
    pixels = image3.load()


    for center_x, center_y in matches:
# range(11) is for the size of the pattern
        for py in range(11):
            for px in range(11):
                if pattern[py][px] == 1:
# center is - 5 since each plus edge is 5 away from the center
                    pixels[(center_x - 5) + px, (center_y - 5) + py] = (255, 0, 0)

    image3.save("IMAGE3.PNG")
    image3.show()
    
    
# -------------- MAIN EXECUTING CODE START -------------- #

inputFileName = GetTextFileName()
print(inputFileName)

try:
    with open("./" + inputFileName, "r") as file:
        if ValidateBinaryFile(file) == False:
            quit()

    # Print the validated file, then save and display IMAGE1.PNG.
    converter = Image1Converter(inputFileName)
    converter.ConvertImage1()
    
    # Print Print provided image2.png
    converter2 = Image2Converter()
    converter2.ConvertImage2()
    
    # Search IMAGE2 and save and display IMAGE3.PNG.
    CreateImage3()
    input("Press Enter to continue...")

except FileNotFoundError:
    print("File not found.")
    input("Press Enter to continue...")
except PermissionError:
    print("Permission denied.")
    input("Press Enter to continue...")
except OSError as e:
    print(f"Could not open file: {e}")
    input("Press Enter to continue...")

# -------------- MAIN EXECUTING CODE END -------------- #

    
    
    
    
    
    
