def reshape_error_message(error):
    try:
        error_messages = []
        counter = 0
        for err in error:
            error_messages.append(err + ": ")
            for serr in error[err]:
                error_messages[counter] += serr
            counter += 1
        return error_messages
    except:
        pass
