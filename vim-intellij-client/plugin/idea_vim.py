import vim
import xmlrpclib

IDEA_RPC_HOST = 'http://localhost'
IDEA_RPC_PORT = 63341


# Server proxy


def server():
    server_url = IDEA_RPC_HOST + ':' + str(IDEA_RPC_PORT)
    return xmlrpclib.ServerProxy(server_url).embeditor


# Main functionality (externally invocable)


def resolve():
    file_path = current_file_path()
    row, col = get_caret_position()
    file_content = current_buffer_content()
    results = server().resolve(file_path, file_content, row, col)

    # todo: replace with for and add popup
    if len(results) > 0:
        result = results[0]
        if result['path'] != file_path:
            # todo: add file existing checking
            vim.command(":e %s" % result['path'])
        set_caret_position(result['line'], result['column'])


def complete():
    find_start = int(vim.eval('a:findstart'))
    base_string = vim.eval('a:base')

    file_path = current_file_path()
    row, col = get_caret_position()
    file_content = (current_buffer_content_before_position(row, col) +
                    base_string +
                    current_buffer_content_after_position(row, col))

    server_method = ('getCompletionStartOffsetInLine' if find_start else
                     'getCompletionVariants')

    result = getattr(server(), server_method)(file_path, file_content, row, col)

    vim.command('return %s' % result)


# Vim-interfacing functions


def current_file_path():
    return vim.eval('expand("%:p")')


def get_caret_position():
    # todo: col should consider tabwidth
    return to_standard_coordinates(*vim.current.window.cursor)


def set_caret_position(line, column):
    if line < len(vim.current.buffer):
        vim.current.window.cursor = to_vim_coordinates(line, 0)
        if column < len(vim.current.buffer[line]):
            vim.current.window.cursor = to_vim_coordinates(line, column)


def current_buffer_content():
    return '\n'.join(vim.current.buffer)


def current_buffer_content_before_position(row, col):
    first_lines = vim.current.buffer[:row]
    current_line_before_position = vim.current.buffer[row][:col]
    return '\n'.join(first_lines + [current_line_before_position])


def current_buffer_content_after_position(row, col):
    current_line_after_position = vim.current.buffer[row][col:]
    last_lines = vim.current.buffer[row + 1:]
    return '\n'.join([current_line_after_position] + last_lines)


# Utility


def to_vim_coordinates(row, col):
    '''Transform from standard coordinates to vim coordinates.'''
    return (row + 1, col)


def to_standard_coordinates(row, col):
    '''Transform from vim coordinates to standard coordinates.'''
    return (row - 1, col)
