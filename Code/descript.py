class Descriptor:
    def __set_name__(self, cls, name):
        print(f'Creating descriptor with name {name!r}')
        self.name = name

    def __get__(self, instance, cls):
        print(f'Calling {self.name}.__get__')

    def __set__(self, instance, value):
        print(f'Calling {self.name}.__set__ with value {value!r}')

    def __delete__(self, instance):
        print(f'Calling {self.name}.__delete__')


class Foo:
    a = Descriptor()
    b = Descriptor()
    c = Descriptor()
