from jinja2 import Environment, FileSystemLoader

class TemplatedRequest:
  def render_response(self, template, context=None):
    import os
    template_dirs = [os.path.join(os.path.dirname(__file__),'..','..', 'templates')]
    env = Environment(loader = FileSystemLoader(template_dirs))
    if context is None:
      return self.response.out.write(env.get_template(template).render())
    else:
      return self.response.out.write(env.get_template(template).render(context))
      
def IPNumToQuad(n,pad=3):
    "convert long int to dotted quad string paded with pad 0s"
    d = 256 * 256 * 256
    q = []
    while d > 0:
        m,n = divmod(n,d)
        q.append(str(m).rjust(pad,'0'))
        d = d/256
    return '.'.join(q)
    
def IPQuadToNum(ip):
    "convert decimal dotted quad string to long integer works with any number of padded 0s"
    hexn = ''.join(["%02X" % long(i) for i in ip.split('.')])
    return long(hexn, 16)

def IPencode(ip_address): # around 10% faster than IPQuadToNum
    return reduce((lambda ip, part: (ip << 8) | int(part)), ip_address.split('.'), 0)

def IPdecode(addr):
    return '.'.join(map(lambda (bits, ip): str((ip >> bits) & 255), [(i*8, addr) for i in range(4)])[::-1])
