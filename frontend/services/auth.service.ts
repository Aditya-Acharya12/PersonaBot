import api from "@/lib/api";

export const login = async (email: string, password: string) => {
  const form = new URLSearchParams();
  form.append("username", email);   // email goes here
  form.append("password", password);

  const res = await api.post("/auth/token", form, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  return res.data as {
    access_token: string;
    token_type: string;
  };
};

export async function signup(
  name: string,
  email: string,
  password: string
) {
  const res = await api.post("/auth/signup", {
    name,
    email,
    password,
  });
  return res.data;
}
