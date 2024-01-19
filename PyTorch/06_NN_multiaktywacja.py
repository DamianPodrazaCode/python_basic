import torch
from torch import nn
import matplotlib.pyplot as plt 
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split
from helper_functions import plot_decision_boundary

torch.manual_seed(42)  # ziarnistość random
torch.cuda.manual_seed(42) # to samo tylko dla cuda

device = "cuda" if torch.cuda.is_available() else "cpu" # wybranie urządzenia liczącego

# wygenerowanie dwóch punktowych okręgów (tuple), pierwsza tablica ma wszystkie współrzędn punktów (X dane wejściowe), 
# a druga dane rozróżniające te punkty, 1 to jedno koło a 0 to drugie koło (y dane wyjściowe), dane są wymieszane pozycjami
n_samples = 1000 
X, y = make_circles(n_samples, noise=0.03, random_state=42) 

# konwersja do tensorów
X = torch.from_numpy(X).type(torch.float)
y = torch.from_numpy(y).type(torch.float)

# rozdzielenie na dane uczenia i testu
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42) 

# tensory do właściwego urządzenia
X_train, y_train = X_train.to(device), y_train.to(device)
X_test, y_test = X_test.to(device), y_test.to(device)

# tworzenie instancji sieci neuronowej za pomocą sekwencji
modelNN = nn.Sequential(
    nn.Linear(in_features=2, out_features=128),
    nn.ReLU(),  # funkcja relu która wykonuje się pomiędzy warstwani, łamie liniowość
    nn.Linear(in_features=128, out_features=128),
    nn.ReLU(),  
    nn.Linear(in_features=128, out_features=1),
).to(device)

# ustawienie funkcji strat i optymalizacji
loss_fn = nn.BCEWithLogitsLoss() 
optimizer = torch.optim.SGD(params=modelNN.parameters(), lr=0.2)

# pętla uczenia
epochs = 500
for epoch in range(epochs):
    
    # uczenie
    modelNN.train()
    y_out = modelNN(X_train).squeeze() 
    loss = loss_fn(y_out, y_train)
    optimizer.zero_grad()
    loss.backward() 
    optimizer.step()

    # Końcowa funkcja aktywacji, uzależniona od tego jakie chcemy uzyskać dane wyjściowe
    y_sigmoid = torch.sigmoid(y_out) # dane po sigmoidzie przedział (0,1)
    y_relu = torch.relu(y_out) # dane po relu przedział (0,+)
    # zaokrąglenie do 0 albo 1
    y_pred = torch.round(y_sigmoid) # tylko to prawidłowo zadziała ponieważ sigmoid jest w przedziale (0,1)

#wizualizacja
print(loss) # poziom strat

plt.figure('Wizualizacja', figsize=(12, 8)) # tytuł i rozmiar plota
plt.subplots_adjust(left=0.05, bottom=0.05, top=0.95, right=0.95) # dociągnięcie do ramek wykresów

plt.subplot(2, 3, 1)
plt.title("Podział obszarów, nauka.")
plot_decision_boundary(modelNN, X_train, y_train)

plt.subplot(2, 3, 2)
plt.title("Gołe dane")
plt.scatter(x=X_train[:, 0].cpu(), y=X_train[:, 1].cpu(), c=y_out.cpu().detach().numpy(), s=4, cmap=plt.cm.RdYlBu)

plt.subplot(2, 3, 3)
plt.title("Sigmoida")
plt.scatter(x=X_train[:, 0].cpu(), y=X_train[:, 1].cpu(), c=y_sigmoid.cpu().detach().numpy(), s=4, cmap=plt.cm.RdYlBu)

plt.subplot(2, 3, 4)
plt.title("ReLU")
plt.scatter(x=X_train[:, 0].cpu(), y=X_train[:, 1].cpu(), c=y_relu.cpu().detach().numpy(), s=4, cmap=plt.cm.RdYlBu)

plt.subplot(2, 3, 5)
plt.title("1 - 0")
plt.scatter(x=X_train[:, 0].cpu(), y=X_train[:, 1].cpu(), c=y_pred.cpu().detach().numpy(), s=4, cmap=plt.cm.RdYlBu)

plt.show()
