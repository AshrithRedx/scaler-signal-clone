import api from "./api";

export const ChatAPI = {

    async login(phone: string) {

        const response = await api.post(
            "/auth/login",
            {
                phone_number: phone,
            }
        );

        return response.data;

    },

    async verifyOTP(
        phone: string,
        otp: string,
    ) {

        const response = await api.post(
            "/auth/verify-otp",
            {
                phone_number: phone,
                otp,
            }
        );

        return response.data;

    },

    async getConversations(
        userId: string,
    ) {

        const response =
            await api.get(
                `/conversations?user_id=${userId}`
            );

        return response.data;

    },

    async getMessages(
        conversationId: string,
    ) {

        const response =
            await api.get(
                `/messages/${conversationId}`
            );

        return response.data;

    }

};