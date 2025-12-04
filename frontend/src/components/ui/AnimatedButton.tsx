'use client';

import { motion, MotionProps } from 'framer-motion';
import { ButtonHTMLAttributes, ReactNode } from 'react';

// Combine motion props and standard button attributes
type AnimatedButtonProps = ButtonHTMLAttributes<HTMLButtonElement> &
  MotionProps & {
    children: ReactNode;
    className?: string;
  };

const AnimatedButton = ({
  children,
  className = '',
  ...props
}: AnimatedButtonProps) => {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      transition={{ type: 'spring', stiffness: 400, damping: 17 }}
      className={`
        px-6 py-3 rounded-lg
        font-semibold
        text-white dark:text-black
        bg-black dark:bg-white
        focus:outline-none focus:ring-2 focus:ring-offset-2
        dark:focus:ring-gray-500
        transition-colors duration-300
        ${className}
      `}
      {...props}
    >
      {children}
    </motion.button>
  );
};

export default AnimatedButton;
