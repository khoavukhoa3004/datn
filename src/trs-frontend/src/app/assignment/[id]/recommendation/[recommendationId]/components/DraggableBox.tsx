import { useState } from "react";
interface DraggleBoxProps {
  ids: number[];
}

const DraggleBox: React.FC<DraggleBoxProps> = ( ids ) => {
  const [isBoxDragged, setIsBoxDragged] = useState(false);

  const handleBoxDragStart = () => {
    setIsBoxDragged(true);
  };

  const handleBoxDragEnd = () => {
    setIsBoxDragged(false);
  };

  const handleDropBox = (event: any) => {
    event.preventDefault();
    setIsBoxDragged(false);
  };

  const handleDragOver = (event: any) => {
    event.preventDefault();
  };

  return (
    <div>
      <div className="bg-yellow-400 w-90 h-95">
        hello
      </div>
      <div className="flex flex-row">
        <div>
          Item 1
        </div>
        <div>
          Item 2
        </div>
      </div>
    </div>
  );
};


export default DraggleBox;