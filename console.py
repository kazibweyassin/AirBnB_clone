#!/usr/bin/python3
""" Airbnb clone interpreter """
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Entry point for the command interpreter for the AirBnB clone """
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """ command to exit the program """
        return True

    def emptyline(self):
        """ Nothing is done when an empty line is entered """
        pass

    def do_EOF(self, arg):
        """ Uses Ctrl-D (EOF) to exit the program """
        print("")
        return True

    def do_crete(self, arg):
        """ Creates a new instance of BaseModel, saves it in the JSON file """
        if not arg:
            print("** class name missing **")
            return

        if arg not in globals():
            print("** class doesn't exist **")
            return
        obj = globals()[arg]()
        obj.save()
        print(obj.id)

    def do_show(self, arg):
        """ The string representation of an instance is printed """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in globals():
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key in storage.all():
            print(storage.all()[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """ Deletes an instance based on class name and saves the changes into the JSON file:(structure: [class name] [id] """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in globals():
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """ All string representations of instances is printed """
        args = arg.split()
        if not args:
            print([str(obj) for obj in storage.all().values()])
        elif args[0] in globals():
            print([str(obj) for key, obj in globals()[args[0]].all().item()])
        else:
            print("** class doesn't exist **")


    def do_update(self, arg):
        """ Updates an instance based on class name and id by adding or updating attribute:(saves changes to JSON file) """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in globals():
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        try:
            update_dict = eval('{' + ' '.join(args[3:]) + '}')
        except:
            print("** invalid dictionary format **")
            return

        for k, v in update_dict.items():
            setattr(storage.all()[key], k, v)
        storage.all()[key].save()

    def do_count(self, arg):
        """ Counts number of instances of a class """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] in globals():
            count = len(globals()[args[0]].all())
            print(count)
        else:
            print("** class doesn't exist **")


    def default(self, line):
        """ Handles new ways of inputing data """
        args = line.split('.')
        if len(args) > 1 and args[0] in globals() and args[1] == "show":
            cls_name = args[0]
            if len(args) < 3:
                print("** instance id missing **")
                return
            key = "{}.{}".format(cls_name, args[2])
            if key in storage.all():
                print(storage.all[key])
            else:
                print("** no instance found **")
        else:
            print("*** Unknown syntax: {}".format(line))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
