" load plugin if vim compiled with +python
if !has('python')
	echo "Error: Required vim compiled with +python"
	finish
endif

" load plugin only once
if exists("g:loaded_intellij") || &cp
    finish
endif
let g:loaded_intellij = 1

command! -nargs=* Python :python <args>

" initialize idea_vim plugin
Python << ENDPYTHON
import vim
import sys
sys.path.insert(0, vim.eval('expand("<sfile>:p:h")'))
import idea_vim
ENDPYTHON

" START COMPLETION
function! idea#complete(findstart, base)
  Python idea_vim.complete()
endfunction

augroup intellijintegration
    autocmd!
    autocmd FileType java,javascript setlocal omnifunc=idea#complete
    autocmd FileType java,javascript nmap <buffer> <C-]> :Python idea_vim.resolve()<CR>
augroup end
