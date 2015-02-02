'''ZeusMP 1D simulation output file class.  Assumes circular polars'''

from twod_plan_file import zeus_file

class zeus1d_file(zeus_file):
    
    def open_rho(self):
        self.rho = self._open_array("gas density")[0,0,:] #1D
        return self.rho
        
    def open_e(self):
        self.e   = self._open_array(" gas energy")[0,0,:] #1D
        return self.e
        
    def open_v_x(self):
        self.v_x = self._open_array(" i velocity")[0,0,:] #1D
        return self.v_x    
    
    def open_coords(self):
        super(zeus1d_file,self).open_coords()
        self.r = self.x
        
    def _line_out(self,var,theta):
        self.open_coords()
        
        return self.r, var  
    
    def open_v_r(self):
        self.v_r = self.open_v_x()
        return self.v_r