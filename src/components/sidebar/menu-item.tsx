import { cn } from '@/lib/utils'
import Link from 'next/link'
import React from 'react'

type Props = {
  size: 'max' | 'min'
  label: string
  icon: JSX.Element
  path?: string
  current?: string
  onSignOut?(): void
}

const MenuItem = ({ size, path, icon, label, current, onSignOut }: Props) => {
  switch (size) {
    case 'max':
      return (
        <Link
          onClick={onSignOut}
          className={cn(
            'flex items-center gap-3 px-4 py-2 rounded-lg my-1 transition-colors',
            !current
              ? 'text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800'
              : current === path
              ? 'bg-white font-bold text-black'
              : 'text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800'
          )}
          href={path ? `/${path}` : '#'}
        >
          {icon} {label}
        </Link>
      )
    case 'min':
      return (
        <Link
          onClick={onSignOut}
          className={cn(
            'flex items-center justify-center p-2 rounded-lg my-1 transition-colors',
            !current
              ? 'text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800'
              : current === path
              ? 'bg-white font-bold text-black'
              : 'text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800'
          )}
          href={path ? `/${path}` : '#'}
        >
          {icon}
        </Link>
      )
    default:
      return null
  }
}

export default MenuItem
