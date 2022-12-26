

class Encrypt:
    def _init_(self) -> None:
        pass

class Decrypt:
    
    # messages={
    #     "10"{
    #         "totalChunk":5,
    #         "currentChunk":3,   #no of chunks available
    #         "chunks":['','']   //without header and crc
    #     }
    # }
    allMessages={}
    
    def reflect_data(x):
        x = ((x & 0x55) << 1) | ((x & 0xAA) >> 1)
        x = ((x & 0x33) << 2) | ((x & 0xCC) >> 2)
        x = ((x & 0x0F) << 4) | ((x & 0xF0) >> 4)
        return x
    
    def crc_poly(self,data, n, poly, crc=0, ref_in=False, ref_out=False, xor_out=0):
        
        try:
            # Hex Decimal to Byte
            data = bytes.fromhex(data)
        except:
            print("In valid Hex String!")
            return -1
        
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
        return hex(crc ^ xor_out)

    def decrypter(self,chunk):
        
        # Removing Accidental Spaces
        chunk=chunk.replace(" ", "")
        
        #Slicing the headers from a Block
        AppId=chunk[:2]
        messageId=int(chunk[2:4], base=16)
        totalChunk=int(chunk[6:8], base=16)
        currentChunkNo=int(chunk[8:10], base=16)
        
        # print(totalChunk,currentChunkNo)
        data=chunk[10:-2]
        crc8=chunk[-2:]
        
        #Printing All the headers
        print("AppId: ", AppId)
        print("MessageId: ", messageId)
        print("Total Number of Blocks: ", totalChunk)
        print("Current Block Number", currentChunkNo)
        
        # IF the Current Block Number Exceed Total Number of Blocks Throw an Error
        if(currentChunkNo > totalChunk):
            print("[Error]: The Current Block Number Exceed the total Block Number!!!\n")
            return # Return Error Happen
        
        # Else
        m=str(self.crc_poly(chunk[:-2],8, 0x07))[2:]
        if(len(m)==1):
            m="0"+m
        # print(m,crc8)
        if(crc8.upper()!=m.upper()):
            print("[Error]: ERC Error occured")
            
        else:
            if(self.allMessages.get(messageId)==None):
                # print(appId,messageId)

                chunks=['']*int(totalChunk)
                chunks[int(currentChunkNo)-1]=data
                self.allMessages[messageId]={
                    "totalChunk":int(totalChunk),
                    "currentChunk":1,
                    "chunks":chunks
                }
            else:
                # update existing chunk for message id
                chunks=self.allMessages[messageId]["chunks"]
                if(data in chunks):
                    print("[Error]: duplicate message")
                else:
                    self.allMessages[messageId]["currentChunk"]+=1
                    chunks[int(currentChunkNo)-1]=data
                    self.allMessages[messageId]["chunks"]=chunks
                    # print(self.allMessages[messageId]["currentChunk"],self.allMessages[messageId]["totalChunk"])
                    if(self.allMessages[messageId]["currentChunk"]==self.allMessages[messageId]["totalChunk"]):
                        # The Actual message
                        print()
                        print("#############################The Actual Message########################\n")
                        print("".join(chunks),"\n")
                    


if __name__=="__main__":
    # For automatic test
    def test(chunk):
        d=Decrypt()
        for i in chunk:
            result=d.decrypter(i)
        
    chunks_array=[
        [
        '01136007010102030405060708091122334455C4',
        '011360070266778899AABBCCDDEEFF0102030407',
        '0113600707445566778899AABBCCDDEEFFA3',
        '011360070509112233445566778899AABBCCDD02',
        '0110730901000100010030006b6169a109060703',
        '0110730909f471804C',
        '011073090260857405080103a203020100a305F6',
        '0110730903a10302010e8802078089076085743D',
        '011073090538393a3b3c3d3e3f4041a40a04085E',
        '011073090405080202aa128010323334353637B4',
        '0113600706EEFF01020304050607080911223303',
        '0113600706EEFF01020304050607080911223393',
        '01107309064953453039333033be230421281fBB',
        '0110730907300000000202eaa8204de6095da6B9',
        '0113600704AABBCCDDEEFF01020304050607083E',
        '0113600704AABBCCDDEEFF01020304050607083E',
        '0113600703050607080911223344556677889937',
        '0110730908488859d6ecadd05637f4da9aac7522'
    ],
    [
        '01123204010123456789AAAABBBBCCCCDDDDEE01',
        '01123204010123456789AAAABBBBCCCCDDDDEE01',
        '0112320402EEFFFFAAAABBBBCCCCDDDDEEEEFF81',
        '0112320402EEFFFFAAAABBBBCCCCDDDDEEEEFF82',
        '0112320403FFAAAABBBBCCCCDDDDEEEEFFFFAA5B',
        '0112320404AABBBBCCCCDDDDEE18'
    ],
    ['0174730901000100010030006b6169a109060709', 
            '017473090260857405080103a203020100a3057C', 
            '0174730903a10302010e880207808907608574A3', 
            '017473090405080202aa12801032333435363762', 
            '017473090538393a3b3c3d3e3f4041a40a040874', 
            '01747309064953453039333033be230421281fFF', 
            '0174730907300000000202eaa8204de6095da692', 
            '0174730908488859d6ecadd05637f4da9aac7566', 
            '0174730909f471801E'
            ]
    ]
    
    option = input("Enter the Option Test(0) manual(1): ")
    if option == "0":
        testNumber = 1
        for chunks in chunks_array:
            print(testNumber)
            testNumber+=1
            test(chunks)
    else:
        decoder = Decrypt()
        print() #New Line
        print("#######################Reassembly#######################")
        while(True):
            
            print() #New Line
            chunk = input("chunk: ")
            decoder.decrypter(chunk)
            
    
