from jinja2 import Environment, FileSystemLoader

class TemplatedRequest:
  def render_response(self,template, **kwargs):
    import os
    template_dirs = [os.path.join(os.path.dirname(__file__),'..','..', 'templates')]
    env = Environment(loader = FileSystemLoader(template_dirs))
    return self.response.out.write(env.get_template(template).render(kwargs))
