import React from 'react';
import './LogModal.css';

function LogModal({ isOpen, onClose, children }: Props) {
	if (!isOpen) return null;
	
	return (
		<div onClick={onClose} className='modal'>
			<div className='modal-content'>
				<span className='close'>&times;</span>
				{children}
			</div>
		</div>
	);
}

export default LogModal;
