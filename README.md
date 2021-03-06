# `django-boss`

`django-boss` is an implementation of the ideas outlined in [my blog post][0] on
Django management commands. With `django-boss`, you can specify commands in
individual apps and then run them using the `djboss` command-line interface.

  [0]: http://blog.zacharyvoase.com/2009/12/09/django-boss/

## News

#### 0.6.1

If `settings.DEBUG` is `True`, the default logging level will be set to `DEBUG`.
Otherwise it will be `WARN`.

### 0.6

`django-boss` is now free and unencumbered software released into the public
domain.

### 0.5

You can now use the `MODEL_LABEL` argparse type to define arguments which take
model specifiers. The arguments object will contain the model class. For
example:

    from djboss.commands import *
    
    @command
    @argument('model', type=MODEL_LABEL)
    def print_model(args):
        """Print the class object for a specified model."""
        print args.model

Could be run like this:

    $ djboss print-model auth.user
    <class 'django.contrib.auth.User'>

Model specifiers take the form `app_label.model_name`, where `model_name` is
case-insensitive.

### 0.4

You can now use the `APP_LABEL` argparse type to define an argument which takes
the name of an installed Django app; the attribute on the arguments object will
hold the appropriate module object. For example, this:

    from djboss.commands import *
    
    @command
    @argument('app', type=APP_LABEL)
    def print_app(args):
        """Print the module object for a specified app."""
        print args.app

Would run like this:

    $ djboss print-app auth
    <module 'django.contrib.auth' from '/.../auth/__init__.pyc'>

### 0.2

`django-boss` now comes with a `manage` command that lets you run *native*
Django management commands under `djboss`. For example:

    $ djboss manage --help
    $ djboss manage syncdb
    $ djboss manage runserver --help

So you can (if you want) delete the `./manage.py` file in your project and use
`djboss` exclusively!

## Installing `django-boss`

At the moment, installation is done via `easy_install django-boss` or
`pip install django-boss`. The only prerequisites are
[argparse](http://argparse.googlecode.com), whose installation is handled by
setuptools, and [Django](http://djangoproject.com/), which you should have 
installed by now anyway.

## Writing Commands

Commands are defined as instances of `djboss.commands.Command`, present in a
`commands` submodule inside an installed app. For example, take the following
app layout:

    echoapp/
    |-- __init__.py
    |-- commands.py
    `-- models.py

The `commands.py` file is a submodule that can be imported as
`echoapp.commands`.

### With Decorators

The following is a complete example of a valid `commands.py` file:

    from djboss.commands import *
    
    @command
    def hello(args):
        """Print a cliche to the console."""
        
        print "Hello, World!"

This example uses the `@command` decorator to declare that the function is a
`django-boss` command. You can add arguments to commands too; just use the
`@argument` decorator (make sure they come *after* the `@command`):

    @command
    @argument('-n', '--no-newline', action='store_true',
              help="Don't append a trailing newline.")
    def hello(args):
        """Print a cliche to the console."""
        
        if args.no_newline:
            import sys
            sys.stdout.write("Hello, World!")
        else:
            print "Hello, World!"

The `@argument` decorator accepts whatever
`argparse.ArgumentParser.add_argument()` does; consult the [argparse docs][1]
for more information.

  [1]: http://argparse.googlecode.com/svn/tags/r101/doc/add_argument.html

You can also annotate commands by giving keyword arguments to `@command`:

    @command(name="something", description="Does something.")
    def do_something(args):
        """Do something."""
        
        print "something has been done."

In this case, the command will be called `"something"` instead of the
auto-generated `"do-something"`, and its description will differ from its
docstring. For more information on what can be passed in here, consult the
[argparse.ArgumentParser docs][2].

  [2]: http://argparse.googlecode.com/svn/tags/r101/doc/ArgumentParser.html

### Without Decorators

The API is very similar without decorators. The `Command` class is used to wrap
functions, and you can give keyword arguments when invoking it as with
`@command`:

    def echo(args):
        ...
    echo = Command(echo, name='...', description='...')

Adding arguments uses the `Command.add_argument()` method, which is just a
reference to the generated sub-parser’s `add_argument()` method:

    def echo(args):
        ...
    echo = Command(echo, name='...', description='...')
    echo.add_argument('-n', '--no-newline', ...)
    echo.add_argument('words', nargs='*')

## Running Commands

Commands are executed via the `djboss` command-line interface. For this to run
correctly, you need one of two things:

*   A `DJANGO_SETTINGS_MODULE` environment variable which refers to a valid,
    importable Python module.
*   A valid, importable `settings` module in the current working directory.

Once one of those is covered, you can run it:

    $ djboss --help
    usage: djboss [-h] [-v] [-l LEVEL] COMMAND ...
    
    Run django-boss management commands.
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -l LEVEL, --log-level LEVEL
                            Choose a log level from DEBUG, INFO, WARN (default)
                            or ERROR.
    
    commands:
      COMMAND
        echo                Echo the arguments back to the console.
        hello               Print a cliche to the console.
    
    To discover sub-commands, djboss first finds and imports your Django settings.
    The DJANGO_SETTINGS_MODULE environment variable takes precedence, but if
    unspecified, djboss will look for a `settings` module in the current
    directory. Commands should be defined in a `commands` submodule of each app.
    djboss will search each of your INSTALLED_APPS for management commands.

Each subcommand gets a `--help` option too:

    $ djboss echo --help
    usage: djboss echo [-h] [-n] [words [words ...]]
    
    Echo the arguments back to the console.
    
    positional arguments:
      words
    
    optional arguments:
      -h, --help        show this help message and exit
      -n, --no-newline  Don't print a newline afterwards.

And then you can run it:

    $ djboss echo some words here
    some words here

More of the same:

    $ djboss hello --help
    usage: djboss hello [-h]
    
    Print a cliche to the console.
    
    optional arguments:
      -h, --help  show this help message and exit

And finally:

    $ djboss hello
    Hello, World!

## (Un)license

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
