import React from 'react'

type MenuLogoProps = {
  onClick(): void
}

export const MenuLogo = ({ onClick }: MenuLogoProps) => {
  return (
    <svg
      onClick={onClick}
      width="30"
      height="30"
      viewBox="0 0 110 110"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect x="5" y="5" width="100" height="100" rx="10" ry="10" fill="#f3d299" stroke="orange" strokeWidth="10"/>
      <path d="M65 10 L30 60 H55 L45 100 L80 50 H55 L65 10" fill="orange" stroke="orange" strokeWidth="2" strokeLinejoin="round"/>
    </svg>
  )
}