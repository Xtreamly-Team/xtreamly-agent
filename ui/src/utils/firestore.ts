import {app} from "./ga";
import {
    collection as fCollection,
    getFirestore,
    onSnapshot,
    query,
} from "firebase/firestore";

const db = getFirestore(app);

export function subscribeTo(collection: string, onUpdate: (data: { string: any }) => void) {
    const q = query(fCollection(db, collection));
    return onSnapshot(q, (snapshot: any) => {
        const data: any = {}
        snapshot.forEach((doc: any) => {
            data[doc.id] = doc.data()
        });
        onUpdate(data)
    });
}
