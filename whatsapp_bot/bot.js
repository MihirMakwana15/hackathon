const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require("@whiskeysockets/baileys")
const { Boom } = require("@hapi/boom")
const qrcode = require("qrcode-terminal")
const axios = require("axios")

async function startBot() {

    const { state, saveCreds } = await useMultiFileAuthState("auth")

    const sock = makeWASocket({
        auth: state
    })

    sock.ev.on("creds.update", saveCreds)

    sock.ev.on("connection.update", (update) => {
        const { connection, lastDisconnect, qr } = update

        // 🔹 Show QR manually
        if (qr) {
            console.log("📱 Scan this QR code:\n")
            qrcode.generate(qr, { small: true })
        }

        if (connection === "close") {
            const shouldReconnect =
                (lastDisconnect?.error instanceof Boom)?.output?.statusCode !== DisconnectReason.loggedOut

            if (shouldReconnect) {
                console.log("Reconnecting...")
                startBot()
            } else {
                console.log("Logged out.")
            }

        } else if (connection === "open") {
            console.log("✅ WhatsApp Bot Connected")
        }
    })

    sock.ev.on("messages.upsert", async (m) => {

    if (m.type !== "notify") return;

    const msg = m.messages[0];

    if (!msg.message) return;
    if (msg.key.fromMe) return;

    const from = msg.key.remoteJid;

    const text =
        msg.message.conversation ||
        msg.message.extendedTextMessage?.text;

    if (!text) return;

    console.log("User:", text);

    try {
        const response = await axios.post("http://127.0.0.1:8000/process", {
            text: text,
            phone: from
        });

        await sock.sendMessage(from, {
            text: response.data.reply
        });

    } catch (error) {
        console.log("Backend error:", error.message);

        await sock.sendMessage(from, {
            text: "⚠️ Server error. Please try again."
        });
    }
});

}

startBot()
