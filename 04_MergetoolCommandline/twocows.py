import cmd
import shlex
import cowsay



class TwoCowsShell(cmd.Cmd):
    intro = 'Добро пожаловать в TwoCows Shell. Введите help или ? для получения справки.\n'
    prompt = 'twocows> '

    def do_exit(self, arg):
        print("До свидания!")
        return True

    def do_quit(self, arg):
        return self.do_exit(arg)

    def do_EOF(self, arg):
        print()
        return self.do_exit(arg)

    def do_list_cows(self, arg):
        """Выводит список доступных персонажей (коров)

        Использование: list_cows
        """
        print("Доступные персонажи:")
        print(", ".join(cowsay.list_cows()))

    def complete_cowsay(self, text, line, begidx, endidx):
        return self._complete_cow_name(text)

    def complete_cowthink(self, text, line, begidx, endidx):
        return self._complete_cow_name(text)

    def _complete_cow_name(self, text):
        all_cows = cowsay.list_cows()
        if not text:
            return all_cows
        else:
            return [cow for cow in all_cows if cow.startswith(text)]

    def do_make_bubble(self, arg):
        """Создает пузырь с текстом

        Использование: make_bubble сообщение
        """
        args = shlex.split(arg)
        if not args:
            print("Ошибка: не указано сообщение")
            return

        message = args[0]
        bubble = cowsay.make_bubble(message)
        print(bubble)

    def do_cowsay(self, arg):
        """Персонаж говорит сообщение.

        Использование:
        cowsay сообщение [имя_персонажа [параметр=значение ...]] reply ответ [имя_персонажа [параметр=значение ...]]

        Примеры:
        cowsay "Привет!"
        cowsay "Привет!" tux
        cowsay "Привет!" tux eyes="XX" reply "Здравствуйте!" dragon"""
        args = self._parse_cow_command(arg)
        if not args:
            return

        cow1_lines = self._generate_cow_lines(
            args['message1'],
            args.get('cow1', 'default'),
            args.get('cow1_params', {})
        )

        if 'message2' in args:
            cow2_lines = self._generate_cow_lines(
                args['message2'],
                args.get('cow2', 'default'),
                args.get('cow2_params', {})
            )

            self._adjust_cow_heights(cow1_lines, cow2_lines)

            for i in range(len(cow1_lines)):
                print(f"{cow1_lines[i]} {cow2_lines[i]}")
        else:
            for line in cow1_lines:
                print(line)


    def do_cowthink(self, arg):
        """Персонаж думает сообщение

        Использование:
        cowthink сообщение [имя_персонажа [параметр=значение ...]] reply ответ [имя_персонажа [параметр=значение ...]]

        Примеры:
        cowthink "О чем я думаю..."
        cowthink "О чем я думаю..." sheep
        cowthink "О чем я думаю..." sheep eyes="^^" reply "Интересно..." turtle
        """
        args = self._parse_cow_command(arg)
        if not args:
            return

        cow1_lines = self._generate_cow_lines(
            args['message1'],
            args.get('cow1', 'default'),
            args.get('cow1_params', {}),
            think=True
        )

        if 'message2' in args:
            cow2_lines = self._generate_cow_lines(
                args['message2'],
                args.get('cow2', 'default'),
                args.get('cow2_params', {}),
                think=True
            )

            self._adjust_cow_heights(cow1_lines, cow2_lines)

            for i in range(len(cow1_lines)):
                print(f"{cow1_lines[i]} {cow2_lines[i]}")
        else:
            for line in cow1_lines:
                print(line)

    def _parse_cow_command(self, arg):
        tokens = shlex.split(arg)
        if not tokens:
            print("Ошибка: не указано сообщение")
            return None

        result = {'message1': tokens[0]}

        idx = 1
        cow1_params = {}

        if idx < len(tokens) and tokens[idx] != 'reply':
            result['cow1'] = tokens[idx]
            idx += 1

            while idx < len(tokens) and tokens[idx] != 'reply':
                if '=' in tokens[idx]:
                    param, value = tokens[idx].split('=', 1)
                    cow1_params[param] = value
                idx += 1

        if cow1_params:
            result['cow1_params'] = cow1_params

        if idx < len(tokens) and tokens[idx] == 'reply':
            idx += 1
            if idx < len(tokens):
                result['message2'] = tokens[idx]
                idx += 1

                cow2_params = {}
                if idx < len(tokens):
                    result['cow2'] = tokens[idx]
                    idx += 1

                    while idx < len(tokens):
                        if '=' in tokens[idx]:
                            param, value = tokens[idx].split('=', 1)
                            cow2_params[param] = value
                        idx += 1

                if cow2_params:
                    result['cow2_params'] = cow2_params

        return result

    def _generate_cow_lines(self, message, cow_name, params, think=False):
        cow_func = cowsay.cowthink if think else cowsay.cowsay

        kwargs = {'message': message, 'cow': cow_name}

        for param, value in params.items():
            if param in ['eyes', 'tongue']:
                kwargs[param] = value

        cow_text = cow_func(**kwargs)
        return cow_text.split('\n')

    def _adjust_cow_heights(self, cow1_lines, cow2_lines):
        cow1_height = len(cow1_lines)
        cow2_height = len(cow2_lines)

        cow1_max_len = max(len(line) for line in cow1_lines)
        cow2_max_len = max(len(line) for line in cow2_lines)

        if cow1_height < cow2_height:
            padding = cow2_height - cow1_height
            for _ in range(padding):
                cow1_lines.insert(0, " " * cow1_max_len)
        elif cow2_height < cow1_height:
            padding = cow1_height - cow2_height
            for _ in range(padding):
                cow2_lines.insert(0, " " * cow2_max_len)

        for i in range(len(cow1_lines)):
            padding = cow1_max_len - len(cow1_lines[i])
            if padding > 0:
                cow1_lines[i] += " " * padding


if __name__ == '__main__':
    TwoCowsShell().cmdloop()