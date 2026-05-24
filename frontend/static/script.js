document.addEventListener("DOMContentLoaded", () => {
  const themeToggle = document.getElementById("themeToggle");
  const sidebar = document.getElementById("sidebar");
  const sidebarAction = document.getElementById("sidebarAction");
  const body = document.body;

  const tabButtons = document.querySelectorAll(".tab-button");
  const tabSections = {
    chats: document.getElementById("chats"),
    docs: document.getElementById("docs")
  };

  const chatForm = document.getElementById("chatForm");
  const chatLog = document.getElementById("chatLog");
  const questionInput = document.getElementById("questionInput");

  // Lists inside sidebar for chats and docs
  const chatsList = document.getElementById("chatsList");
  const docsList = document.getElementById("docsList");

  // Hidden file input for PDF upload
  const fileUpload = document.createElement("input");
  fileUpload.type = "file";
  fileUpload.accept = ".pdf";
  fileUpload.style.display = "none";
  document.body.appendChild(fileUpload);

  // Current active chat name
  let activeChat = null;

  // Utility: create list item with delete button
  function createListItem(name, type) {
    const item = document.createElement("div");
    item.className = type === "chat" ? "chat-item" : "doc-item";

    // Use a span for text to allow delete button separate
    const textSpan = document.createElement("span");
    textSpan.textContent = name;
    item.appendChild(textSpan);

    // Delete button
    const delBtn = document.createElement("button");
    delBtn.className = "delete-btn";
    delBtn.textContent = "×";
    delBtn.title = "Delete";

    delBtn.onclick = (e) => {
      e.stopPropagation(); // prevent triggering item click
      if (confirm(`Delete this ${type}?`)) {
        item.remove();
        if (type === "chat") {
          // Remove chat from localStorage and clear chat log if active
          const chats = JSON.parse(localStorage.getItem("chats") || "[]");
          const index = chats.indexOf(name);
          if (index > -1) {
            chats.splice(index, 1);
            localStorage.setItem("chats", JSON.stringify(chats));
          }
          if (activeChat === name) {
            activeChat = null;
            chatLog.innerHTML = "";
          }
        }
        // For docs, deletion backend API can be implemented if needed
      }
    };

    item.appendChild(delBtn);

    // Click on chat item loads that chat
    item.onclick = () => {
      if (type === "chat") {
        loadChat(name);
      } else {
        alert(`You clicked on document: "${name}"`);
      }
    };

    return item;
  }

  // Load chats from localStorage and populate sidebar
  function loadChats() {
    const chats = JSON.parse(localStorage.getItem("chats") || "[]");
    chatsList.innerHTML = "";
    chats.forEach(chatName => {
      const chatItem = createListItem(chatName, "chat");
      chatsList.appendChild(chatItem);
    });
  }

  // Save chat list to localStorage
  function saveChats(chats) {
    localStorage.setItem("chats", JSON.stringify(chats));
  }

  // Save chat log for a chat
  function saveChatLog(chatName, logHtml) {
    localStorage.setItem(`chatlog_${chatName}`, logHtml);
  }

  // Load chat log for a chat
  function loadChat(chatName) {
    activeChat = chatName;
    // Highlight active chat in sidebar
    Array.from(chatsList.children).forEach(child => {
      child.classList.toggle("active", child.textContent.includes(chatName));
    });
    // Load chat log from localStorage
    const logHtml = localStorage.getItem(`chatlog_${chatName}`) || "";
    chatLog.innerHTML = logHtml;
  }

  // Load uploaded documents from backend
  async function loadDocs() {
    try {
      const res = await fetch("/uploads");
      const data = await res.json();
      if (data.files && Array.isArray(data.files)) {
        docsList.innerHTML = "";
        data.files.forEach(fileName => {
          const docItem = createListItem(fileName, "doc");
          docsList.appendChild(docItem);
        });
      }
    } catch (error) {
      console.error("Failed to load documents:", error);
    }
  }

  // Handle tab switching
  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const selectedTab = btn.dataset.tab;

      // Switch active button styling
      tabButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      // Show selected tab section, hide others
      Object.keys(tabSections).forEach(id => {
        tabSections[id].classList.add("hidden");
      });
      tabSections[selectedTab].classList.remove("hidden");

      // Change sidebar action button text and behavior
      if (selectedTab === "chats") {
        sidebarAction.textContent = "+ New Chat";
        sidebarAction.onclick = () => {
          const chats = JSON.parse(localStorage.getItem("chats") || "[]");
          const chatName = `Chat ${chats.length + 1}`;
          const newChat = createListItem(chatName, "chat");
          chatsList.appendChild(newChat);
          chats.push(chatName);
          saveChats(chats);
          loadChat(chatName);
        };
      } else {
        sidebarAction.textContent = "Upload";
        sidebarAction.onclick = () => fileUpload.click();
      }
    });
  });

  // Dark mode toggle button (moon/sun emoji)
  themeToggle.onclick = () => {
    body.classList.toggle("dark");
    themeToggle.textContent = body.classList.contains("dark") ? "☀️" : "🌙";
  };

  // Chat form submission handler
  chatForm.onsubmit = async (e) => {
    e.preventDefault();
    const question = questionInput.value.trim();
    if (!question) return;

    if (!activeChat) {
      alert("Please select or create a chat first.");
      return;
    }

    // Append user question to chat log
    const userMsg = document.createElement("div");
    userMsg.className = "bot-message";
    userMsg.innerHTML = `<div class="bubble" style="background:#dbeafe">${question}</div><div class="timestamp">You • just now</div>`;
    chatLog.appendChild(userMsg);
    chatLog.scrollTop = chatLog.scrollHeight;

    questionInput.value = "";

    // Send question to backend and get answer
    try {
      const res = await fetch("/ask", {
        method: "POST",
        body: new URLSearchParams({ question })
      });
      const data = await res.json();

      // Append bot answer to chat log
      const botMsg = document.createElement("div");
      botMsg.className = "bot-message";
      botMsg.innerHTML = `<div class="bubble">${data.answer || "Sorry, something went wrong."}</div><div class="timestamp">Bot • just now</div>`;
      chatLog.appendChild(botMsg);
      chatLog.scrollTop = chatLog.scrollHeight;

      // Save chat log
      saveChatLog(activeChat, chatLog.innerHTML);
    } catch {
      const botMsg = document.createElement("div");
      botMsg.className = "bot-message";
      botMsg.innerHTML = `<div class="bubble">Sorry, something went wrong.</div><div class="timestamp">Bot • just now</div>`;
      chatLog.appendChild(botMsg);
      chatLog.scrollTop = chatLog.scrollHeight;

      // Save chat log
      saveChatLog(activeChat, chatLog.innerHTML);
    }
  };

  // File upload input change handler
  fileUpload.onchange = async () => {
    const file = fileUpload.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/upload", {
        method: "POST",
        body: formData
      });
      const data = await res.json();

      if (data.message) {
        // Add uploaded document to docs list
        const newDoc = createListItem(file.name, "doc");
        docsList.appendChild(newDoc);
      } else if (data.error) {
        alert(data.error);
      }
    } catch {
      alert("Upload failed. Please try again.");
    }
  };

  // Load chats and docs on page load
  loadChats();
  loadDocs();

  // Initialize default tab to Chats on page load
  tabButtons[0].click();
});
