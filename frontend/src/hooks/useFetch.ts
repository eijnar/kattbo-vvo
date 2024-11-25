// src/hooks/useFetch.ts

import { useState, useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";

interface FetchState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

const useFetch = <T,>(url: string): FetchState<T> => {
  const { getAccessTokenSilently, isAuthenticated } = useAuth0();
  const [state, setState] = useState<FetchState<T>>({
    data: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    let isMounted = true;

    const fetchData = async () => {
      try {
        setState({ data: null, loading: true, error: null });
        const headers: HeadersInit = {};

        if (isAuthenticated) {
          const token = await getAccessTokenSilently();
          headers.Authorization = `Bearer ${token}`;
        }

        const response = await fetch(url, { headers });

        const contentType = response.headers.get("Content-Type");
        if (!contentType || !contentType.includes("application/json")) {
          // Log the unexpected content type
          const text = await response.text();
          console.error(`Unexpected Content-Type: ${contentType}`);
          console.error(`Response Text: ${text}`);
          throw new Error("Received non-JSON response");
        }

        if (!response.ok) {
          const errorText = await response.text();
          console.error(`Error ${response.status}: ${response.statusText}`);
          console.error(`Error Response Text: ${errorText}`);
          throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const data: T = await response.json();
        if (isMounted) {
          setState({ data, loading: false, error: null });
        }
      } catch (error: any) {
        if (isMounted) {
          setState({ data: null, loading: false, error: error.message });
        }
        console.error("Fetch error:", error);
      }
    };

    fetchData();

    return () => {
      isMounted = false;
    };
  }, [url, getAccessTokenSilently, isAuthenticated]);

  return state;
};

export default useFetch;
