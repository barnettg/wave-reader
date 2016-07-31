# Reads a wave file
# verifies sample rate and other header information
# prints a C array of uint8, without header
# prints variable with array size

## wave file header
##Byte Number 	offset      Size 	Description 	    Value
##0-3 	         0-3         4 	        Chunk ID 	    "RIFF" (0x52494646)
##4-7 	         4-7         4 	        Chunk Data Size     (file size) - 8
##8-11 	         8-11        4 	        RIFF Type 	    "WAVE" (0x57415645) 
##
##
##Byte Number 	            Size 	Description 	    Value
##0-3 	        12-15       4 	        Chunk ID 	    "fmt " (0x666D7420)
##4-7 	        16-19       4 	        Chunk Data Size     Length Of format Chunk (always 0x10)
##8-9 	        20-21       2 	        Compression code    Always 0x01
##10 - 11 	22-23       2 	        Channel Numbers     0x01=Mono, 0x02=Stereo
##12 - 15 	24-27       4 	        Sample Rate 	    Binary, in Hz
##16 - 19 	28-31       4 	        Bytes Per Second 	 
##20 - 21 	32-33       2 	        Bytes Per Sample    1=8 bit Mono, 2=8 bit Stereo or 16 bit Mono, 4=16 bit Stereo
##22 - 23 	34-35       2 	        Bits Per Sample 	 
##
##Byte Number 	            Size 	Description 	    Value
##0-3 	        36-39       4 	        Chunk ID 	    "data" (0x64617461)
##4-7 	        40-43       4 	        Chunk Data Size     length of data to follow
##8-end 	44-end	                Data 	            sound samples
  	  	  	 

class waveFile:
    
    def __init__(self):
      self.btArray = []
      self.btArrayLength = 0

    def verifyHeader(self):
        reply = True
        if chr(self.btArray[0]) == 'R' and chr(self.btArray[1]) == 'I' and \
            chr(self.btArray[2]) == 'F' and chr(self.btArray[3]) == 'F':
            print ("RIFF OK")
        else:
            print ("RIFF error")
            reply = False

        if chr(self.btArray[8]) == 'W' and chr(self.btArray[9]) == 'A' and \
            chr(self.btArray[10]) == 'V' and chr(self.btArray[11]) == 'E':
            print ("WAVE OK")
        else:
            print ("WAVE error")
            reply = False

        sampleRate = self.btArray[27] 
        sampleRate = sampleRate << 8
        sampleRate = sampleRate + self.btArray[26]
        sampleRate = sampleRate << 8
        sampleRate = sampleRate + self.btArray[25]
        sampleRate = sampleRate << 8
        sampleRate = sampleRate + self.btArray[24] 

        print ("Sample rate %d HZ"%sampleRate)

        dataSize = self.btArray[43] 
        dataSize = dataSize << 8
        dataSize = dataSize + self.btArray[42]
        dataSize = dataSize << 8
        dataSize = dataSize + self.btArray[41]
        dataSize = dataSize << 8
        dataSize = dataSize + self.btArray[40]
        self.btArrayLength = dataSize

        print ("data size %d bytes"%dataSize)

        self.btArray = self.btArray[44:]

        
        #return False # temporary for faster dev
        return reply

    def getWavFile(self):
        reply = True
        filename=input("Enter the file name: ")
        fh = None
        try:
            fh = open(filename, 'rb')
            self.btArray = bytearray(fh.read())
        except:
            reply = False    
        finally:
            if fh != None:
                fh.close()
                
        return reply

    
    def writeData(self):
        reply = True
        outfilename=input("Enter the output file name: ")
        arrayname = input("Enter the array name name: ")
        outF = None
        try:
            outF = open(outfilename, 'w')
            varname = "uint16 " + arrayname+"Size = " + str(self.btArrayLength) + ";\n"
            outF.write(varname)
            outF.write("const uint8 %s[ ] = {\n" % arrayname)
            
            line = 0
            for byte in self.btArray:
                #print ("%d, " % byte, end = '')
                outF.write("%3d, " % byte)
                line = line +1
                if line>15:
                    #print ("")
                    outF.write("\n")
                    line = 0
            outF.write("0 };\n")
        except:
            reply = False 
        finally:
            if outF != None:
                outF.close()
        
        return reply
    
        
    def start(self):
        if self.getWavFile() == False:
            print ("wave file error!!")
            return
        
        if self.verifyHeader() == False:
            print ("Header error!!")
            return
        
        if self.writeData() == False:
            print ("Write Data error!!")
            return
        
        print ("Done")


if __name__ == "__main__":
    print ("hello")
    wf = waveFile()
    wf.start()






    ##        filename=input("Enter the file name: ")
##        outfilename=input("Enter the output file name: ")
##        arrayname = input("Enter the array name name: ")
##        ba = []
##
##        try:
##            fh = open(filename, 'rb')
##            outF = open(outfilename, 'w')
##            ba = bytearray(fh.read())
##            verifyHeader(ba)
##
##            line = 0
##            for byte in ba:
##                #print ("%d, " % byte, end = '')
##                outF.write("%d, " % byte)
##                line = line +1
##                if line>15:
##                    #print ("")
##                    outF.write("\n")
##                    line = 0
##        finally:
##            fh.close()
##            outF.close()
##            
##        #outF.close()
##        #fh.close()

