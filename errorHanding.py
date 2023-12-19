#TODO error handling
#make wrapper function to do error handeling 

def errorWrapper(func):

    def wrap(*args,**kwargs):

        try:
            func(*args,**kwargs)
        except FileNotFoundError: #if file is not found
            print("fuck off")
        except FileExistsError: #if written file alreadty exists, might not be a problem since function are writing over them
            pass
        except IndexError:
            pass
        except KeyError:
            pass

        else:
            pass
        finally:
            pass
    return wrap