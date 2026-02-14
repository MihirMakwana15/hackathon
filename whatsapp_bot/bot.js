const { default: makeWASocket, useMultiFileAuthState } = require("@whiskeysockets/baileys")
const axios = require("axios")

async function startBot() {

    const { state, saveCreds } = await useMultiFileAuthState("auth")
    const sock = makeWASocket({ auth: state })

    sock.ev.on("creds.update", saveCreds)

    sock.ev.on("messages.upsert", async ({ messages }) => {

        const msg = messages[0]
        if (!msg.message) return

        const text = msg.message.conversation
        const from = msg.key.remoteJid

        if (!text) return

        const response = await axios.post("http://localhost:8000/process", {
            text: text,
            phone: from
        })

        await sock.sendMessage(from, {
            text: response.data.reply
        })
    })
}

startBot()
