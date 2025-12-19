import React from 'react';
import { motion } from 'framer-motion';

const Button = ({ 
  children, 
  onClick, 
  variant = 'primary', 
  size = 'md', 
  icon, 
  disabled = false,
  className = '',
  ...props 
}) => {
  const variants = {
    primary: {
      base: 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg shadow-purple-500/25',
      hover: 'hover:from-purple-600 hover:to-pink-600 hover:shadow-xl hover:shadow-purple-500/40',
      active: 'active:from-purple-700 active:to-pink-700'
    },
    secondary: {
      base: 'bg-slate-700 text-white border border-slate-600 shadow-lg shadow-slate-500/25',
      hover: 'hover:bg-slate-600 hover:border-slate-500 hover:shadow-xl hover:shadow-slate-500/40',
      active: 'active:bg-slate-800'
    },
    success: {
      base: 'bg-green-500 text-white shadow-lg shadow-green-500/25',
      hover: 'hover:bg-green-600 hover:shadow-xl hover:shadow-green-500/40',
      active: 'active:bg-green-700'
    },
    info: {
      base: 'bg-blue-500 text-white shadow-lg shadow-blue-500/25',
      hover: 'hover:bg-blue-600 hover:shadow-xl hover:shadow-blue-500/40',
      active: 'active:bg-blue-700'
    },
    warning: {
      base: 'bg-yellow-500 text-white shadow-lg shadow-yellow-500/25',
      hover: 'hover:bg-yellow-600 hover:shadow-xl hover:shadow-yellow-500/40',
      active: 'active:bg-yellow-700'
    },
    danger: {
      base: 'bg-red-500 text-white shadow-lg shadow-red-500/25',
      hover: 'hover:bg-red-600 hover:shadow-xl hover:shadow-red-500/40',
      active: 'active:bg-red-700'
    }
  };

  const sizes = {
    sm: 'px-4 py-2 text-sm min-h-[36px]',
    md: 'px-6 py-3 text-base min-h-[44px]',
    lg: 'px-8 py-4 text-lg min-h-[52px]',
    xl: 'px-12 py-5 text-xl min-h-[60px]'
  };

  const currentVariant = variants[variant];

  return (
    <motion.button
      whileHover={{ 
        scale: disabled ? 1 : 1.02,
        y: disabled ? 0 : -2
      }}
      whileTap={{ 
        scale: disabled ? 1 : 0.98,
        y: disabled ? 0 : 0
      }}
      transition={{
        type: "spring",
        stiffness: 400,
        damping: 17
      }}
      onClick={disabled ? undefined : onClick}
      className={`
        ${currentVariant.base}
        ${currentVariant.hover}
        ${currentVariant.active}
        ${sizes[size]} 
        ${disabled ? 'opacity-50 cursor-not-allowed grayscale' : 'cursor-pointer'}
        rounded-full font-semibold transition-all duration-300 ease-out
        flex items-center gap-3 justify-center
        transform-gpu will-change-transform
        focus:outline-none focus:ring-4 focus:ring-purple-500/30
        select-none
        ${className}
      `}
      disabled={disabled}
      {...props}
    >
      {icon && (
        <motion.span 
          className="flex-shrink-0"
          whileHover={{ rotate: variant === 'primary' ? 5 : 0 }}
          transition={{ duration: 0.2 }}
        >
          {icon}
        </motion.span>
      )}
      <span className="font-medium tracking-wide">{children}</span>
    </motion.button>
  );
};

export default Button;