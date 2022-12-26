import random 

#Globals
ChunkSize = 20
# Message_ID = random.sample(range(0, 1000), 100)
messageIDList = []


class Fragment:
    def __init__ (self, string_Data):
        self.string_Data = string_Data
        # Header Datas
        self.AppId = "01"
        self.messageId = random.randint(0,255)
        self.totalLen = len(string_Data)//2
        # Need Calculate
        self.totalBlock = 0
        self.allchunks = [] #To Store the all chunks
        self.message = []
        # If the messageId already taken take a new one randomly
        while(self.messageId in messageIDList):
            self.messageId = random.randint(0,255)

        messageIDList.append(self.messageId)
    
    # To reflect the Data
    def reflect_data(x):
        x = ((x & 0x55) << 1) | ((x & 0xAA) >> 1)
        x = ((x & 0x33) << 2) | ((x & 0xCC) >> 2)
        x = ((x & 0x0F) << 4) | ((x & 0xF0) >> 4)
        return x
    
    def crc_poly(self,data, n, poly ):
        
        crc=0
        ref_in=False
        ref_out=False
        xor_out=0
            # Hex Decimal to Byte
        data = bytes.fromhex(data)
        
        
        # print("hex",data)
        g = 1 << n | poly  # Generator polynomial
        # Loop over the data
        for d in data:
            # Reverse the input byte if the flag is true
            if ref_in:
                d = self.reflect_data(d, 8)
            # XOR the top byte in the CRC with the input byte
            crc ^= d << (n - 8)
            # Loop over all the bits in the byte
            for _ in range(8):
                # Start by shifting the CRC, so we can check for the top bit
                crc <<= 1
                # XOR the CRC if the top bit is 1
                if crc & (1 << n):
                    crc ^= g
        # Reverse the output if the flag is true
        if ref_out:
            crc = self.reflect_data(crc, n)

        # Return the CRC value as hex value
        # print(hex(crc ^ xor_out))
        return crc ^ xor_out
    
    def formatToString(self, num):
            hex_num = hex(num)
            string = str(hex_num)[2:].upper()
            if len(string) <2:
                string = "0" + string
            return string
    
    # Split the String in to messages
    def splitString(self):
        messageSizePerChunk = (ChunkSize - 6)*2 #chunkSize - HeaderSize = messageSize
        self.message = [self.string_Data[i:i+messageSizePerChunk] for i in range(0, len(self.string_Data), messageSizePerChunk)]
        # print( self.totalLen)
        self.totalBlock = len(self.message)
        
    def createChunks(self):
        # If not splitString is already called
        if self.totalBlock ==0:
            self.splitString()
        
        # Formating the Headers
        messageId = self.formatToString(self.messageId)
        totalLen = self.formatToString(self.totalLen)
        totalBlock = self.formatToString(self.totalBlock)
        
        #Print all the Details of the HexString
        print("App ID: ",self.AppId)
        print("Maximum Chunk Size(Dec): ", ChunkSize)
        print("messageId(Dec): ", self.messageId)
        print("total length of Hex String(Dec): ", self.totalLen)
        print("Total number of blocks(Dec): ", self.totalBlock)
        
        # Add Header To all Messages in the self.messages
        for i in range (self.totalBlock):
            # Adding First 5 headers
            current_Block = self.formatToString(i+1)
            chunk = self.AppId + messageId + totalLen +totalBlock + current_Block + self.message[i] 
            # Calculating crc8
            crc8 = self.crc_poly(chunk,8, 0x07)
            crc8 = self.formatToString(crc8)
            # Adding last Header CRC-8 
            chunk = chunk + crc8
            # Storing all the headers
            chunk = chunk.upper()
            self.allchunks.append(chunk)
        
    # Get A Specific Block/chunk
    def getBlock(self,blockNumber):
        if len(self.allchunks) == 0:
            self.createChunks()
        if(blockNumber> self.totalBlock):
            print("[Error]: Exceed the number of blocks!")
        else:
            print("[Block",blockNumber,"] :- " ,self.allchunks[blockNumber-1]) 
        print() #New Line
    
    # PriintAll chunks
    def printAllchunk(self):
        if len(self.allchunks) == 0:
            self.createChunks()
        
        for i in range (self.totalBlock):
            print("[Block ",(i+1),"] :- " ,self.allchunks[i])
            # print(self.allchunks);
        return 0
    
if __name__=="__main__":
    # test1 ="000100010030006b6169a109060760857405080103a203020100a305a10302010e88020780890760857405080202aa12801032333435363738393a3b3c3d3e3f4041a40a04084953453039333033be230421281f300000000202eaa8204de6095da6488859d6ecadd05637f4da9aac75f47180"
    # test2 = "010203040506070809112233445566778899AABBCCDDEEFF010203040506070809112233445566778899AABBCCDDEEFF010203040506070809112233445566778899AABBCCDDEEFF010203040506070809112233445566778899AABBCCDDEEFF"
    # frag = Fragment(test1)
    # frag.printAllchunk()
    while(True):
        print("")#To print a new Line
        print("##############################FRAGMENTATION################################")
        print("")#To print a new Line
        stringInput = input("Enter the Hex String: ")
        print("") #To print a new Line
        options  = input("Return All Chunk (0) OR Return a specific chunck (Any): ")
        
        # Create the Object
        frag = Fragment(stringInput)
        if options=="0":
            frag.printAllchunk()
        else:    
            frag.createChunks()
            blockNumber = int(input("Enter the block Number(from 1 to " +str(frag.totalBlock)+" ): "))
            frag.getBlock(blockNumber)

