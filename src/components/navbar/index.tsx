'use client'

import Image from 'next/image';
import * as React from 'react';
import { Button } from '../ui/button';
import Link from 'next/link';
import { useState } from 'react';

// WIP: change settings link to dashboard link
function NavBar() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <div className="flex gap-5 justify-between items-center px-7 py-1 font-bold border-b border-solid border-zinc-100 leading-[154.5%] max-md:px-5">
      {/* Logo */}
      <div className="flex gap-1.5 justify-center self-stretch my-auto text-2xl tracking-tighter text-neutral-700">
        <Image
          src="/images/logo.png"
          alt="LOGO"
          sizes="100vw"
          style={{
            width: '150px',
            height: 'auto',
          }}
          width={0}
          height={0}
        />
      </div>

      {/* Desktop Menu */}
      <ul className="gap-5 justify-between self-stretch my-auto text-sm leading-5 text-neutral-700 font-normal hidden md:flex">
        <li>Home</li>
        <li>Pricing</li>
        <li>News Room</li>
        <li>Features</li>
        <li>Contact us</li>
      </ul>

      {/* Mobile Menu Icon */}
      <div className="md:hidden">
        <button onClick={toggleMobileMenu} className="text-neutral-700">
          {isMobileMenuOpen ? (
            <span>&#x2715; {/* Close icon */}</span>
          ) : (
            <span>&#9776; {/* Hamburger icon */}</span>
          )}
        </button>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <ul className="flex flex-col gap-3 absolute top-14 left-0 w-full bg-white p-5 text-neutral-700 md:hidden">
          <li onClick={toggleMobileMenu}>Home</li>
          <li onClick={toggleMobileMenu}>Pricing</li>
          <li onClick={toggleMobileMenu}>News Room</li>
          <li onClick={toggleMobileMenu}>Features</li>
          <li onClick={toggleMobileMenu}>Contact us</li>
        </ul>
      )}

      {/* Sign Up Button */}
      <Button asChild className="bg-orange px-4 py-2 rounded-sm text-white hidden md:block">
        <Link href="/dashboard">Try Now</Link>
      </Button> 

      {/* <Link 
      href="/settings"
      className='bg-orange px-4 py-2 rounded-sm text-white'
      >
      Try Now
      </Link> */}
    </div>
  );
}

export default NavBar;
