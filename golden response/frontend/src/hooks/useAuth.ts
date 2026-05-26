"use client";

import { useCallback } from "react";
import { useDispatch, useSelector } from "react-redux";
import { login as apiLogin, register as apiRegister } from "@/services/api";
import { logout, setCredentials } from "@/store/authSlice";
import { RootState } from "@/store";

export function useAuth() {
  const dispatch = useDispatch();
  const { user, token, isAuthenticated } = useSelector(
    (state: RootState) => state.auth
  );

  const signIn = useCallback(
    async (email: string, password: string) => {
      const res = await apiLogin(email, password);
      dispatch(
        setCredentials({
          user: res.data.user,
          token: res.data.access_token,
        })
      );
      return res.data;
    },
    [dispatch]
  );

  const signUp = useCallback(
    async (name: string, email: string, password: string) => {
      await apiRegister(name, email, password);
      return signIn(email, password);
    },
    [signIn]
  );

  const signOut = useCallback(() => {
    dispatch(logout());
  }, [dispatch]);

  return { user, token, isAuthenticated, signIn, signUp, signOut };
}
