const elements = document.querySelectorAll(".type"); // 选取所有 .type
  const texts = Array.from(elements).map(el => el.innerText.trim()); // 记录文本
  elements.forEach(el => el.innerText = ""); // 先清空文本

  function typeText(index = 0) {
    if (index >= elements.length) return; // 所有段落完成后停止

    const element = elements[index];
    const text = texts[index];
    let i = 0;

    function type() {
      if (i < text.length) {
        element.innerHTML = text.slice(0, i + 1).replace(/\n/g, "<br>");
        i++;
        setTimeout(type, 5); // 速度控制
      } else {
        setTimeout(() => typeText(index + 1), 500); // 等待 0.5s 再开始下一个段落
      }
    }

    type();
  }

  typeText(); // 启动打字效果