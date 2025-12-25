import api from "../api/api";

export const getAnnouncements = async () => {
  const res = await api.get("/announcements/");
  return res.data;
};

export const createAnnouncement = async (data: {
  title: string;
  message: string;
  category?: string;
}) => {
  const res = await api.post("/announcements/", data);
  return res.data;
};

export const updateAnnouncement = async (
  id: number,
  data: { title: string; message: string; category?: string }
) => {
  const res = await api.put(`/announcements/${id}`, data);
  return res.data;
};

export const deleteAnnouncement = async (id: number) => {
  await api.delete(`/announcements/${id}`);
};
