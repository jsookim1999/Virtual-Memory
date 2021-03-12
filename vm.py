# Virtual Memory Manager class

class vmManager:
    def __init__(self, line1, line2, _input):
        self.PM = [None for i in range(524288)]
        self.D = [[None for i in range(512)] for i in range(1024)]
        self.line1 = line1
        self.line2 = line2 
        self._input = _input
        self.result = []
        self.free_frames = {i:0 for i in range(1024)} # frame # : present_bit

    def initialization(self):
        self.init_ST()
        self.init_PT()
        # FOR DEBUGGING:
        # self.show_PM()
        # self.show_D()
        # self.show_FF()

    def init_ST(self):
        self.mark_frame(0,1)
        self.mark_frame(1,1)
        for entry in self.line1:
            segment = entry[0]
            size    = entry[1]
            frame   = entry[2]
            self.PM[2*segment]   = size
            self.PM[2*segment+1] = frame
            if frame > 0:
                self.mark_frame(frame,1)

    def init_PT(self):
        for entry in self.line2:
            segment = entry[0]
            page    = entry[1]
            frame   = entry[2]
            if self.PM[segment*2+1] > 0:
                self.PM[self.PM[segment*2+1]*512+page] = frame
                if frame > 0:
                    self.mark_frame(frame,1)
            else:
                disk_entry = abs(self.PM[segment*2+1])
                self.D[disk_entry][page]= frame
                if frame > 0:
                    self.mark_frame(frame,1)
    
    def tran_VA(self):
        """
        Translate the Virtual addresses into Physical address and store them into self.result
        """
        for va in self._input:
            # print("va:" + str(va)+":")
            s = va >> 18
            p = (va >> 9) & int(b'111111111',2)
            w = va & int(b'111111111',2)
            pw = va & int(b'111111111111111111',2)
            if pw >= self.PM[2*s]:
                self.result.append(str(-1))
            elif self.PM[2*s+1] < 0: # PAGE FAULT: PT IS NOT RESIDENT
                block = abs(self.PM[2*s+1])
                free_frame = self.next_free_frame()
                self.PM[2*s+1] = free_frame # assign new frame
                self.mark_frame(free_frame,1) # mark the frame occupied
                self.read_block(block, free_frame*512) # copy the block into PM 
                if self.PM[free_frame*512 + p] < 0: # if the page is not resident
                    next_free = self.next_free_frame() 
                    self.PM[free_frame*512 + p] = next_free
                    self.mark_frame(next_free,1)
                pg = self.PM[free_frame*512 + p] * 512
                PA = pg + w
                self.result.append(str(PA))
            elif self.PM[self.PM[2*s+1]*512+p] < 0: # PAGE FAULT: PAGE IS NOT RESIDENT
                free_frame = self.next_free_frame()
                self.PM[self.PM[2*s+1]*512+p] = free_frame
                self.mark_frame(free_frame,1)
                PA = free_frame * 512 + w
                self.result.append(str(PA))
            else: 
                PA = self.PM[self.PM[2*s+1]*512+p]*512 + w
                self.result.append(str(PA))
            
            # For debugging:
            # self.show_PM()
            # self.show_D()
            # self.show_FF()

    # HELPER
    def next_free_frame(self):
        for k in sorted(self.free_frames.keys()):
            if self.free_frames[k] == 0:
                return k
    
    def read_block(self,b,m):
        # copy block D[b] fnto PM frame starting at location PM[m]
        for i in range(512):
            self.PM[m + i] = self.D[b][i]
    
    def mark_frame(self, frame_num, p_bit):
        if frame_num >= 0 and frame_num < 1024:
            self.free_frames[frame_num] = p_bit
        else:
            print("ERROR::mark_frame: frame_num out of range")
    
    # OUTPUT RESULT (Used by main.py)
    def output(self):
        return " ".join(self.result)
        
    # FOR DEBUGGING 
    def show_PM(self):
        print("------PM------")
        for i in range(524288):
            if self.PM[i] != None:
                print(str(i)+":"+str(self.PM[i]))
        print("--------------")

    def show_D(self):
        print("-----DISK-----")
        for i,entry in enumerate(self.D):
            s = str(i)+":"
            for e in entry:
                if e != None:
                    s += str(e)
                    s += " "
            if s != str(i)+":":
                print(s)
        print("--------------")
    
    def show_FF(self):
        print("------FF------")
        for k,v in self.free_frames.items():
            if v != 0:
                print("Frame " + str(k) + ": occupied")
        print("--------------")