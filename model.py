import torch


class Model:

    def __init__(self):
        self._model = torch.load("model_data.txt")
        self._loss = torch.nn.CrossEntropyLoss()
        self._optimizer = torch.optim.Adam(self._model.parameters(), lr=1.0e-3)

    def predict(self, image):
        image = image.reshape(1, 1, 28, 28)
        self._preds = self._model.forward(image)
        return self._preds.argmax().item()

    def learn(self, correct_answer):
        correct_answer = torch.tensor([correct_answer])
        loss_value = self._loss(self._preds, correct_answer)
        loss_value.backward()

        self._optimizer.step()

    def save(self):
        torch.save(self._model, "model_data.txt")
