package org.jetbrains.plugins.embeditor

import com.intellij.codeInsight.completion.CompletionParameters
import com.intellij.codeInsight.lookup.LookupElement
import com.intellij.openapi.diagnostic.Logger
import com.intellij.openapi.editor.Document
import com.intellij.util.ArrayUtil

val LOG = Logger.getInstance(javaClass<EmbeditorRequestHandler>())

public class EmbeditorRequestHandler {
  public fun getStartCompletionOffset(path: String, fileContent: String, line: Int, column: Int): Int {
    LOG?.debug("getStartCompletionOffset(${path}:${line}:${column}")
    var result = 0
    EmbeditorUtil.performCompletion(path, fileContent, line, column, object: EmbeditorUtil.CompletionCallback {
      override fun completionFinished(parameters: CompletionParameters,
                                      items: Array<out LookupElement>,
                                      document: Document) {
        val range = parameters.getPosition().getTextRange()
        if (range != null) {
          val offset = range.getStartOffset()
          val lineNumber = document.getLineNumber(offset)
          result = offset - document.getLineStartOffset(lineNumber)
        }
      }
    })
    return result
  }

  public fun getCompletionVariants(path: String, fileContent: String, line: Int, column: Int): Array<String> {
    LOG?.debug("getCompletionVariants(${path}:${line}:${column}")
    var variants: Set<String> = setOf()
    EmbeditorUtil.performCompletion(path, fileContent, line, column, object: EmbeditorUtil.CompletionCallback {
      override fun completionFinished(parameters: CompletionParameters,
                                      items: Array<out LookupElement>,
                                      document: Document) {
        variants = items.map { it.getLookupString() }.toSet()
      }
    })
    return variants.toArray(Array(variants.size, { "" }))
  }
}
