"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.checkConnections = exports.testFirestore = exports.helloWorld = void 0;
const functions = require("firebase-functions");
const admin = require("firebase-admin");
// Initialize admin with emulator configuration
admin.initializeApp({
    projectId: 'ariapp-9ec5b',
    // Point to the emulator
    credential: admin.credential.applicationDefault()
});
// Configure functions to use emulators
process.env.FIRESTORE_EMULATOR_HOST = 'localhost:8080';
process.env.FIREBASE_AUTH_EMULATOR_HOST = 'localhost:9099';
exports.helloWorld = functions.https.onRequest((request, response) => {
    response.send("Hello from Firebase!");
});
// Example function using Firestore
exports.testFirestore = functions.https.onRequest(async (request, response) => {
    try {
        // This will connect to the Firestore emulator
        const db = admin.firestore();
        const testDoc = await db.collection('test').doc('example').get();
        response.json({
            message: "Connected to Firestore emulator",
            data: testDoc.data() || null,
            timestamp: new Date().toISOString()
        });
    }
    catch (error) {
        response.status(500).json({
            error: error
        });
    }
});
exports.checkConnections = functions.https.onRequest(async (request, response) => {
    try {
        // Test Firestore connection
        const db = admin.firestore();
        await db.collection('test').doc('connection-test').set({
            timestamp: admin.firestore.FieldValue.serverTimestamp()
        });
        // Test Auth connection
        await admin.auth().listUsers(1);
        response.json({
            success: true,
            emulators: {
                firestore: process.env.FIRESTORE_EMULATOR_HOST,
                auth: process.env.FIREBASE_AUTH_EMULATOR_HOST
            },
            message: "Successfully connected to all emulators"
        });
    }
    catch (error) {
        response.status(500).json({
            success: false,
            error: error,
            emulators: {
                firestore: process.env.FIRESTORE_EMULATOR_HOST,
                auth: process.env.FIREBASE_AUTH_EMULATOR_HOST
            }
        });
    }
});
//# sourceMappingURL=index.js.map