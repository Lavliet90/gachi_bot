class RepliesToMessages:
    '''
    en: Catches user messages andanswers a couple of catchphrases from the gachi
    ru: Отлавливает сообщения пользователя и дает ответы на пару коронных фраз из гачи
    '''

    def sosi(message):
        if 'соси' in message.text.lower() or 'sosi' in message.text.lower() or \
                'саси' in message.text.lower() or 'sasi' in message.text.lower():
            return f'Сам соси, {message.from_user.first_name}'
            # Только для беседы, в личке не from_user, a chat
        elif 'извини' in message.text.lower() or 'sorry' in message.text.lower() \
                or 'прости' in message.text.lower() or 'прошу прощения' in message.text.lower():
            return f'Sorry for what, {message.from_user.first_name}?'
        else:
            return

    '''
    en: Top 10 by number of messages
    ru: Топ 10 по количеству сообщений
    '''

    def top_10_stats(result):
        if not result:
            return 'Нет данных...'
        else:
            reply_message = '- Топ флудеров:\n'
            for i, item in enumerate(result):
                reply_message += f'{i + 1}: {item[1].strip()} - {item[2]} messages.\n'
            return reply_message

