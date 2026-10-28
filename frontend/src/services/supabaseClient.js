/**
 * Supabase Client & Authentication Service for Inkloom Sentinel
 * Supports Live Supabase Cloud (with Google OAuth)
 * + Zero-Friction Demo Mode (ensuring hackathon judges are never locked out)
 */

import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || '';
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || '';

export const isLiveSupabaseConfigured = Boolean(SUPABASE_URL && SUPABASE_ANON_KEY);

// Real client (if configured)
export const supabase = isLiveSupabaseConfigured
  ? createClient(SUPABASE_URL, SUPABASE_ANON_KEY)
  : null;

// Mock User Profiles for instant Judge evaluation
const DEMO_USERS = {
  creator: {
    id: 'user_demo_creator',
    email: 'piyush.patel@binarybrains.ai',
    name: 'Piyush Patel',
    role: 'Lead Full-Stack Creator',
    avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=Piyush',
    provider: 'google'
  },
  reviewer: {
    id: 'user_demo_reviewer',
    email: 'aryan.ponkiya@binarybrains.ai',
    name: 'Aryan Ponkiya',
    role: 'Lead Brand Custodian',
    avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=Aryan',
    provider: 'google'
  }
};

let currentDemoUser = DEMO_USERS.creator;
let authListeners = [];

export const authService = {
  isLive: isLiveSupabaseConfigured,

  async getCurrentUser() {
    if (isLiveSupabaseConfigured && supabase) {
      const { data: { user } } = await supabase.auth.getUser();
      return user;
    }
    return currentDemoUser;
  },

  async signInWithGoogle() {
    if (isLiveSupabaseConfigured && supabase) {
      return await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: window.location.origin
        }
      });
    }

    // Demo Mode Google Simulation
    currentDemoUser = currentDemoUser.id === 'user_demo_creator' ? DEMO_USERS.reviewer : DEMO_USERS.creator;
    authListeners.forEach(cb => cb(currentDemoUser));
    return { data: { user: currentDemoUser }, error: null };
  },

  async switchRole(roleType = 'reviewer') {
    currentDemoUser = DEMO_USERS[roleType] || DEMO_USERS.creator;
    authListeners.forEach(cb => cb(currentDemoUser));
    return currentDemoUser;
  },

  async signOut() {
    if (isLiveSupabaseConfigured && supabase) {
      await supabase.auth.signOut();
    }
    currentDemoUser = null;
    authListeners.forEach(cb => cb(null));
  },

  onAuthStateChange(callback) {
    authListeners.push(callback);
    callback(currentDemoUser);
    return () => {
      authListeners = authListeners.filter(cb => cb !== callback);
    };
  }
};
