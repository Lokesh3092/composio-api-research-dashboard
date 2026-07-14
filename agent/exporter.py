import os


def export_batch(batch_size=10):

    folder = "data/raw_docs"

    files = sorted(os.listdir(folder))

    batch = []

    for file in files[:batch_size]:

        path = os.path.join(folder, file)

        with open(path, "r", encoding="utf-8") as f:

            text = f.read()

        batch.append(
            {
                "file": file,
                "content": text[:6000]
            }
        )

    return batch