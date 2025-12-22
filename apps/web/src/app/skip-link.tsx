'use client'

import { useCallback, type MouseEventHandler } from 'react'

interface SkipLinkProps {
  targetId?: string
}

export function SkipLink({ targetId = 'main-content' }: SkipLinkProps) {
  const handleClick = useCallback<MouseEventHandler<HTMLAnchorElement>>(
    (event) => {
      const target = document.getElementById(targetId)

      if (!target) {
        return
      }

      event.preventDefault()
      target.focus()
      target.scrollIntoView({ behavior: 'smooth', block: 'start' })
    },
    [targetId],
  )

  return (
    <a className="skipLink" href={`#${targetId}`} onClick={handleClick}>
      Skip to main content
    </a>
  )
}
