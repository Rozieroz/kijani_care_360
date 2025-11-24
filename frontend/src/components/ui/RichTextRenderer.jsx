import React from 'react'

const RichTextRenderer = ({ content, className = '' }) => {
  const renderRichText = (text) => {
    if (!text) return null

    // Split text by lines to handle line breaks properly
    const lines = text.split('\n')
    
    return lines.map((line, lineIndex) => {
      if (!line.trim()) {
        return <br key={lineIndex} />
      }

      // Process the line for rich text formatting
      const processedLine = processTextFormatting(line)
      
      return (
        <div key={lineIndex} className="mb-1">
          {processedLine}
        </div>
      )
    })
  }

  const processTextFormatting = (text) => {
    const parts = []
    let currentIndex = 0
    
    // Regular expressions for different formatting
    const patterns = [
      { regex: /\*\*(.*?)\*\*/g, component: 'bold' },      // **bold**
      { regex: /\*(.*?)\*/g, component: 'italic' },        // *italic*
      { regex: /^#{1,3}\s(.+)$/gm, component: 'heading' }, // # Heading
      { regex: /^•\s(.+)$/gm, component: 'bullet' },       // • Bullet
      { regex: /^\d+\.\s(.+)$/gm, component: 'number' },   // 1. Number
    ]

    // Find all matches
    const allMatches = []
    patterns.forEach(pattern => {
      let match
      const regex = new RegExp(pattern.regex.source, pattern.regex.flags)
      while ((match = regex.exec(text)) !== null) {
        allMatches.push({
          start: match.index,
          end: match.index + match[0].length,
          content: match[1] || match[0],
          type: pattern.component,
          fullMatch: match[0]
        })
      }
    })

    // Sort matches by position
    allMatches.sort((a, b) => a.start - b.start)

    // Remove overlapping matches (keep the first one)
    const nonOverlapping = []
    allMatches.forEach(match => {
      const hasOverlap = nonOverlapping.some(existing => 
        (match.start < existing.end && match.end > existing.start)
      )
      if (!hasOverlap) {
        nonOverlapping.push(match)
      }
    })

    // Build the result
    let lastIndex = 0
    const result = []

    nonOverlapping.forEach((match, index) => {
      // Add text before the match
      if (match.start > lastIndex) {
        const beforeText = text.slice(lastIndex, match.start)
        if (beforeText) {
          result.push(<span key={`text-${index}`}>{beforeText}</span>)
        }
      }

      // Add the formatted match
      result.push(renderFormattedText(match, index))
      lastIndex = match.end
    })

    // Add remaining text
    if (lastIndex < text.length) {
      const remainingText = text.slice(lastIndex)
      if (remainingText) {
        result.push(<span key="remaining">{remainingText}</span>)
      }
    }

    return result.length > 0 ? result : text
  }

  const renderFormattedText = (match, index) => {
    const key = `formatted-${index}`
    
    switch (match.type) {
      case 'bold':
        return (
          <strong key={key} className="font-bold text-primary-700">
            {match.content}
          </strong>
        )
      
      case 'italic':
        return (
          <em key={key} className="italic text-primary-600">
            {match.content}
          </em>
        )
      
      case 'heading':
        return (
          <h4 key={key} className="font-bold text-lg text-primary-800 mt-3 mb-2">
            {match.content}
          </h4>
        )
      
      case 'bullet':
        return (
          <div key={key} className="flex items-start space-x-2 ml-4 my-1">
            <span className="text-primary-600 font-bold mt-1">•</span>
            <span>{match.content}</span>
          </div>
        )
      
      case 'number':
        return (
          <div key={key} className="flex items-start space-x-2 ml-4 my-1">
            <span className="text-primary-600 font-bold">{match.fullMatch.split('.')[0]}.</span>
            <span>{match.content}</span>
          </div>
        )
      
      default:
        return <span key={key}>{match.content}</span>
    }
  }

  return (
    <div className={`rich-text-content ${className}`}>
      {renderRichText(content)}
    </div>
  )
}

export default RichTextRenderer