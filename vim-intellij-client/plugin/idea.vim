let s:IDEA_RPC_HOST="http://localhost"
let s:IDEA_RPC_PORT=63341

if !has('python')
	echo "Error: Required vim compiled with +python"
	finish
endif

function! idea#complete(findstart, base)
	if a:findstart
		" todo: should retrieve base offset from idea
		return col('.') - 1
	else
python << endpython
import vim
import xmlrpclib
server=xmlrpclib.ServerProxy(vim.eval("s:IDEA_RPC_HOST") + ":" + vim.eval("s:IDEA_RPC_PORT"))
# todo: col should consider tabwidth
(row, col) = vim.current.window.cursor
# todo: send whole file to server
result = server.embeditor.getCompletionVariants(vim.eval("expand('%:p')"), row - 1, col)
vim.command("let result=%s" % result)
# todo: error handling
vim.command("return result")
endpython
	endif
endfunction

set completefunc=idea#complete
