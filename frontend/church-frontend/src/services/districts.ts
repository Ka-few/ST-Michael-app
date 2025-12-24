import api from "../api/api";

export const getDistricts = async () => {
  const res = await api.get("/districts/");
  return res.data;
};

export const createDistrict = async (data: {
  name: string;
  leader_name?: string;
}) => {
  const res = await api.post("/districts/", data);
  return res.data;
};
