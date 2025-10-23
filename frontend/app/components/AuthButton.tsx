"use client";

import { useSession, signIn, signOut } from "next-auth/react";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { User, LogOut, Shield } from "lucide-react";
import { toast } from "sonner";

export default function AuthButton() {
  const { data: session, status } = useSession();
  const [manualUser, setManualUser] = useState<{email: string, provider: string} | null>(null);

  // Check for manual authentication on mount
  useEffect(() => {
    const token = localStorage.getItem('zion_auth_token');
    const userData = localStorage.getItem('zion_user_data');
    if (token && userData) {
      try {
        const user = JSON.parse(userData);
        setManualUser(user);
      } catch (err) {
        console.error('Failed to parse user data:', err);
      }
    }
  }, []);

  const handleManualLogout = () => {
    localStorage.removeItem('zion_auth_token');
    localStorage.removeItem('zion_user_data');
    setManualUser(null);
    toast.success('Successfully signed out', {
      duration: 2000,
    });
    window.location.href = '/auth/signin';
  };

  const handleGoogleLogout = () => {
    signOut({ callbackUrl: "/auth/signin" });
    toast.success('Successfully signed out', {
      duration: 2000,
    });
  };

  if (status === "loading") {
    return (
      <div className="flex items-center gap-2 px-3 py-2 text-gray-400">
        <div className="w-4 h-4 border-2 border-gray-400 border-t-transparent rounded-full animate-spin"></div>
        Loading...
      </div>
    );
  }

  // Show Google auth user info
  if (session) {
    return (
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 text-white">
          <User className="w-4 h-4" />
          <span className="text-sm">{session.user?.name || session.user?.email}</span>
          <span className="text-xs bg-blue-600/20 text-blue-300 px-2 py-1 rounded-full">Google</span>
        </div>
        <motion.button
          onClick={handleGoogleLogout}
          className="flex items-center gap-2 px-3 py-2 bg-red-600/20 hover:bg-red-600/30 border border-red-500/30 rounded-lg text-red-300 hover:text-red-200 transition-colors"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <LogOut className="w-4 h-4" />
          Sign Out
        </motion.button>
      </div>
    );
  }

  // Show manual auth user info
  if (manualUser) {
    return (
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 text-white">
          <Shield className="w-4 h-4" />
          <span className="text-sm">{manualUser.email}</span>
          <span className="text-xs bg-green-600/20 text-green-300 px-2 py-1 rounded-full">Manual</span>
        </div>
        <motion.button
          onClick={handleManualLogout}
          className="flex items-center gap-2 px-3 py-2 bg-red-600/20 hover:bg-red-600/30 border border-red-500/30 rounded-lg text-red-300 hover:text-red-200 transition-colors"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <LogOut className="w-4 h-4" />
          Sign Out
        </motion.button>
      </div>
    );
  }

  // Not authenticated - show sign in options
  return (
    <motion.button
      onClick={() => window.location.href = '/auth/signin'}
      className="flex items-center gap-2 px-4 py-2 bg-blue-600/20 hover:bg-blue-600/30 border border-blue-500/30 rounded-lg text-blue-300 hover:text-blue-200 transition-colors"
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
    >
      <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
        <polyline points="10,17 15,12 10,7"/>
        <line x1="15" x2="3" y1="12" y2="12"/>
      </svg>
      Sign In
    </motion.button>
  );
}