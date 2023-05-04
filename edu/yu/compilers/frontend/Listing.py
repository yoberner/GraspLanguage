

class Listing:
    def __init__(self, sourceFileName):
        try:
            file = open(sourceFileName, 'r')
            # BufferedReader br = new BufferedReader(new FileReader(sourceFileName))# TODO
            
            lineNumber = 0
            line = file.readline()# TODO
            
            while line is not None:
                print("%03d %s\n", ++lineNumber, line)
                line = file.readline() # TODO
            
            file.close()# TODO

        except IOError:
            print("ERROR: Failed to open source file \"%s\".\n".format(sourceFileName))
            print("{:s\n".format(IOError.getMessage()))
            exit(-1)
