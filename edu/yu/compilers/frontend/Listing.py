

class Listing:
    def __init__(sourceFileName):
        try:
            BufferedReader br = new BufferedReader(new FileReader(sourceFileName))# TODO
            
            lineNumber = 0
            line = br.readLine()# TODO
            
            while line is not None:
                print("%03d %s\n", ++lineNumber, line)
                line = br.readLine() # TODO
            
            br.close()# TODO

        except IOError:
            print("ERROR: Failed to open source file \"%s\".\n".format(sourceFileName),)
            print("{:s\n".format(IOError.getMessage())
            exit(-1)
